# Local YouTube Summariser 🤖📺

**Summarise YouTube videos instantly and privately** using local LLMs. By running entirely on your own hardware, this tool transcribes and condenses video content without sending any data to the cloud. Keep your data **100% secure, fast, and free**.

## Features
- **Privacy First:** Fully offline execution via local AI models.
- **Auto-Transcription:** Converts video audio to text using OpenAI's Whisper.
- **Smart Summaries:** Generates clean, bulleted insights using Ollama.

## Prerequisites
1. **Python 3.8+**
2. **FFmpeg** installed on your system path (required for audio processing).
3. **Ollama** installed. Download it from [ollama.com](https://ollama.com).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com
   cd youtube-video-summarizer
   ```

2. Install python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download your local LLM of choice (e.g., Llama 3):
   ```bash
   ollama pull llama3.1:latest
   ```

## Usage
Make sure the Ollama application is running in the background, then execute:
```bash
python app.py
```
Paste your target YouTube link when prompted!
