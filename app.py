from fastapi import FastAPI, File, UploadFile
import shutil
import os
import subprocess

app = FastAPI()

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    input_path = f"input_videos/{file.filename}"
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run your main analysis script
    subprocess.run(["python", "main.py"])

    return {"message": "Processing complete! Check output_videos folder."}
