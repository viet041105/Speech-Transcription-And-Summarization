import os
import uuid
import torch
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydub import AudioSegment
from transformers import pipeline
import whisperx
import uvicorn

app = FastAPI(title="Speech-to-Text & Summarization API", description="Convert audio to text and summarize it.")

# Add CORS middleware for ASP.NET Core frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5243"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def prepare_audio_file(input_path, output_path="converted.wav"):
    file_ext = os.path.splitext(input_path)[1].lower()
    if file_ext == ".wav":
        return input_path
    elif file_ext in [".mp3", ".mp4"]:
        try:
            audio = AudioSegment.from_file(input_path)
            audio = audio.set_channels(1).set_frame_rate(16000)
            audio.export(output_path, format="wav")
            return output_path
        except Exception as e:
            print(f"[❌] Audio conversion error: {e}")
            return None
    return None

def summarize_text(text):
    try:
        summarizer = pipeline("summarization", model="t5-small")
        max_input_length = 512
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            current_chunk.append(word)
            current_length += len(word) + 1
            if current_length >= max_input_length:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_length = 0
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        summaries = []
        for i, chunk in enumerate(chunks):
            summary = summarizer(
                "summarize: " + chunk,
                max_length=100,
                min_length=5,
                do_sample=False,
                max_new_tokens=None
            )
            summaries.append(summary[0]['summary_text'])
            print(f"[📝] Summary for chunk {i + 1}: {summary[0]['summary_text']}")

        final_summary = " ".join(summaries)
        print(f"[📝] Final summary: {final_summary}")
        return final_summary
    except Exception as e:
        print(f"[❌] Summarization error: {e}")
        return None

@app.post("/transcribe")
async def transcribe_and_summarize(file: UploadFile = File(...)):
    try:
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)

        input_ext = os.path.splitext(file.filename)[1]
        raw_path = os.path.join(temp_dir, f"{uuid.uuid4()}{input_ext}")

        with open(raw_path, "wb") as f:
            content = await file.read()
            f.write(content)

        wav_path = prepare_audio_file(raw_path, os.path.join(temp_dir, f"{uuid.uuid4()}.wav"))
        if not wav_path:
            raise HTTPException(status_code=400, detail="Unsupported file format or conversion error.")

        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[ℹ️] Using device: {device}")
        model = whisperx.load_model("small", device)
        audio = whisperx.load_audio(wav_path)
        transcription = model.transcribe(audio)

        # Print each transcription segment
        print("[📜] Transcription segments:")
        for i, segment in enumerate(transcription["segments"], 1):
            print(f"Segment {i}: {segment['text'].strip()}")

        full_text = " ".join(seg["text"].strip() for seg in transcription["segments"])
        print(f"[📜] Full transcript: {full_text}")

        summary = summarize_text(full_text)
        if not summary:
            raise HTTPException(status_code=500, detail="Summarization failed.")

        os.remove(raw_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)

        return {
            "transcript": full_text,
            "summary": summary
        }
    except Exception as e:
        if os.path.exists(raw_path):
            os.remove(raw_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)
        print(f"[❌] Error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)