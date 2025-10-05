from fastapi import APIRouter
from ..db import reports, sessions
from ..services import report_service

router = APIRouter()

@router.post("/generate")
async def generate_report(session_id: str):
    sess = await sessions.find_one({"_id": session_id})
    if not sess:
        return {"error": "session not found"}
    pdf_path = report_service.generate_pdf_report(sess)
    # store report metadata
    r = {"session_id": session_id, "path": pdf_path}
    await reports.insert_one(r)
    return {"report_path": pdf_path}