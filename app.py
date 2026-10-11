import os
import yt_dlp
import whisper
import ollama

def download_audio(youtube_url):
    print("⏳ Downloading audio from YouTube...")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    return "temp_audio.mp3"

def transcribe_audio(audio_path):
    print("⏳ Transcribing audio locally with Whisper...")
    model = whisper.load_model("base") 
    result = model.transcribe(audio_path)
    return result["text"]

def generate_summary(transcript):
    print("⏳ Summarising text with local LLM...")
    prompt = f"Summarise the following video transcript clearly with bullet points:\n\n{transcript}"
    
    response = ollama.chat(model='llama3.1:latest', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    return response['message']['content']

def main():
    url = input("Enter YouTube Video URL: ")
    audio_file = download_audio(url)
    
    try:
        transcript = transcribe_audio(audio_file)
        summary = generate_summary(transcript)
        
        print("\n=== 📝 VIDEO SUMMARY ===")
        print(summary)
        
    finally:
        if os.path.exists(audio_file):
            os.remove(audio_file)

if __name__ == "__main__":
    main()