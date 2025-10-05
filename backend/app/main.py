from .routes import interview
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, interview
from .config import settings

app = FastAPI(title="AI Interviewer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock down in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(interview.router, prefix="/interview")
app.include_router(interview.router, prefix="/report")

@app.get("/")
async def root():
    return {"msg":"AI Interviewer backend running"}