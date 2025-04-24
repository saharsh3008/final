from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
import shutil
import subprocess

app = FastAPI()

# Serve the static files from the 'static' folder
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Video Processing App"}

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    # Define where the uploaded file will be stored
    input_path = f"input_videos/{file.filename}"

    # Save the file to the input_videos directory
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run your analysis script after uploading
    subprocess.run(["python", "main.py"])

    return {"message": "Processing complete! Check output_videos folder."}

