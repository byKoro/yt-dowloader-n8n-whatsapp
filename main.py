from fastapi import FastAPI
from fastapi.responses import FileResponse
import yt_dlp
import uuid
import os

app = FastAPI()

@app.get("/download")
def download_video(url: str):
    video_id = str(uuid.uuid4())
    file_path = f"/tmp/{video_id}.mp4"

    ydl_opts = {
        "outtmpl": file_path,
        "format": "mp4",
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web_safari", "default"]
            }
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return {
        "video_id": video_id,
        "download_url": f"/files/{video_id}.mp4"
    }

@app.get("/files/{filename}")
def serve_file(filename: str):
    path = f"/tmp/{filename}"
    if os.path.exists(path):
        return FileResponse(path)
    return {"error": "File not found"}
