from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
from uuid import uuid4
from detect import detect_pizza
from feedback import save_feedback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any domain
    allow_credentials=True,  # Allow cookies to be included in cross-origin requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

UPLOAD_DIR = "data/videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    if not file.filename.endswith(('.mp4', '.avi', '.mov')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only video files are allowed.")

    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        count_result = detect_pizza(file_path)
        return JSONResponse(content={"video_id": file_id, "pizza_count": count_result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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