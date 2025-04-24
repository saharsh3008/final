from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil
import subprocess
import os

app = FastAPI()

# Mount static files (for output videos)
app.mount("/output", StaticFiles(directory="output_videos"), name="output")

# Templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def serve_upload_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    input_dir = "input_videos"
    os.makedirs(input_dir, exist_ok=True)
    input_path = os.path.join(input_dir, file.filename)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run your main processing script
    subprocess.run(["python", "main.py"])

    return {
        "message": "Processing complete!",
        "output_url": f"/output/processed_video.mp4"  # adjust filename accordingly
    }
