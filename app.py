from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
import subprocess
import os

app = FastAPI()

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

    return {"message": "Processing complete! Check output_videos folder."}
