from fastapi import FastAPI, UploadFile, File
import uvicorn
import faster_whisper
import os
import tempfile

app = FastAPI()

# Load model once
model_size = os.getenv("ASR_MODEL", "tiny.en")
device = os.getenv("ASR_DEVICE", "cpu")

model = faster_whisper.WhisperModel(model_size, device=device)

@app.post("/transcribe")
async def transcribe(audio_file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await audio_file.read())
        tmp_path = tmp.name

    segments, info = model.transcribe(tmp_path, word_timestamps=True)
    
    results = []
    for segment in segments:
        results.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })
    
    os.remove(tmp_path)
    
    return {"segments": results}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
