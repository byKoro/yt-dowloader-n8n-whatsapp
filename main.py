from fastapi import FastAPI
import yt_dlp
import uuid
import os

app = FastAPI()

@app.get("/download")
def download_video(url: str):
    video_id = str(uuid.uuid4())
    file_path = f"/app/{video_id}.mp4"

    ydl_opts = {
        "outtmpl": file_path,
        "format": "mp4"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return {
        "video_id": video_id,
        "file_url": f"/files/{video_id}.mp4"
    }

@app.get("/files/{filename}")
def serve_file(filename: str):
    file_full_path = f"/app/{filename}"
    if os.path.exists(file_full_path):
        return FileResponse(file_full_path)
    return {"error": "File not found"}
