from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
from uuid import uuid4
from backend.app.detect import detect_objects
from feedback import save_feedback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any domain
    allow_credentials=True,  # Allow cookies to be included in cross-origin requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.post("/feedback")
async def submit_feedback(video_id: str, frame_id: int, is_correct: bool):
    if not video_id or frame_id is None:
        raise HTTPException(status_code=400, detail="Video ID and frame ID are required.")
    if not isinstance(is_correct, bool):
        raise HTTPException(status_code=400, detail="Correct must be a boolean value.")
    try:
        save_feedback(video_id, frame_id, is_correct)
        return {"message": "Feedback saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "PizzaCounter API is live"}