🚀 Speech-to-Text & Summarization API
Transform any audio or video file into a detailed transcript and an intelligent summary with a single API call. This project provides a powerful and easy-to-use solution for automating the processing and understanding of audio content.

🎥 Demonstration

![z6877610200454_41a3af92163d26239157add23d55baef](https://github.com/user-attachments/assets/e13f05f2-4d9e-48e5-a77d-adae0ffb3d4b)

![z6877609997445_b65d4de8515c61d1e37297e44f72f850](https://github.com/user-attachments/assets/1f944193-cf9b-4e6a-8fcb-5538a1f888dd)




✨ Key Features
Multi-format Conversion: Supports popular file formats like .mp3, .mp4, and .wav.

High Accuracy: Utilizes the WhisperX model for superior transcription accuracy.

Intelligent Summarization: Employs the T5-small model from Hugging Face to generate concise, coherent summaries that retain the core message of the content.

Long-form Content Handling: Automatically chunks the input text to process long audio files, bypassing model input length limitations.

RESTful Interface: The API is built on FastAPI, ensuring high performance and easy integration into any application.

Hardware Optimization: Automatically leverages an available GPU (CUDA) to accelerate processing.

🛠️ Architecture & Technology Stack
The system is built on a combination of leading AI models and libraries:

Component	Technology	Role
Backend Framework	FastAPI	For building a high-performance, asynchronous API.
Web Server	Uvicorn	ASGI server to run the FastAPI application.
Speech-to-Text	WhisperX (Model: small)	An enhanced version of OpenAI's Whisper for improved speed and accuracy.
Text Summarization	Hugging Face Transformers (Model: t5-small)	A powerful Transformer model for text summarization tasks.
Audio Processing	Pydub	Processes and converts various audio formats into the standard WAV format (16kHz, mono).

Xuất sang Trang tính
⚙️ How It Works
File Ingestion: The client sends an audio file (.mp3, .mp4, .wav) to the /transcribe endpoint via a POST request.

Audio Normalization: Pydub converts the input audio file into a standardized .wav format (16kHz, 1-channel mono) to ensure compatibility with the Whisper model.

Transcription: WhisperX loads the normalized .wav file and performs the speech-to-text conversion.

Text Chunking: Because summarization models have input length limits, the full transcript is divided into smaller "chunks".

Summarization: Each text chunk is fed into the t5-small model to generate a summary for that specific chunk.

Result Aggregation: The individual summaries are then combined to form the final, complete summary.

JSON Response: The API returns a JSON object containing the full transcript (transcript) and the final summary (summary).

📦 Installation Guide
Clone the repository:

Bash

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install Python dependencies:
Create a requirements.txt file with the following content and run the pip install command:

Ini, TOML


