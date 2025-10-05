from fastapi import APIRouter, UploadFile, File
from ..services import llm_service, speech_service, emotion_audio, scoring_engine, report_service
from ..db import sessions

router = APIRouter()

@router.post("/start")
async def start_interview(payload: dict):
    # payload: {user_id, interview_type}
    session = {
        "user_id": payload.get("user_id"),
        "type": payload.get("interview_type", "general"),
        "questions": [],
  "answers": [],
        "scores": {},
        "status": "started"
    }
    res = await sessions.insert_one(session)
    session["_id"] = str(res.inserted_id)
    return {"session": session}

@router.post("/ask")
async def ask_question(session_id: str):
    # generate a question via LLM
    q = llm_service.generate_question()
    await sessions.update_one({"_id": session_id}, {"$push": {"questions": q}})
    return {"question": q}

@router.post("/answer")
async def submit_answer(session_id: str, audio: UploadFile = File(...)):
    """
    Accepts audio (wav/m4a), runs STT, emotion analysis, scoring, and returns feedback.
 """
    # save audio to disk (tmp)
    content = await audio.read()
    fname = f"/tmp/{audio.filename}"
    with open(fname, "wb") as f:
        f.write(content)

    transcript = await speech_service.transcribe_audio_file(fname)
    audio_emotion = emotion_audio.analyze_audio(fname)
    # simple content evaluation
    content_score = llm_service.evaluate_answer(transcript)
    # response dynamics (fillers, latency) — placeholder
    rd_score = scoring_engine.compute_response_dynamics(transcript)

    # compute final using weights (default)
    final_score = scoring_engine.compute_final_score(
        cq=content_score, ce=audio_emotion["score"], nvc=5, rd=rd_score
    )

    # update session doc
    await sessions.update_one({"_id": session_id}, {"$push": {"answers": {"transcript":transcript, "score": final_score}}})
    
    return {"transcript": transcript, "emotion": audio_emotion, "score": final_score}