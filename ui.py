import os
import yt_dlp
import whisper
import ollama
import gradio as gr

def process_video(youtube_url, whisper_model, llm_model):
    if not youtube_url:
        return "⚠️ Please enter a valid YouTube URL.", ""
    
    audio_file = "temp_audio.mp3"
    
    # 1. Download Audio
    try:
        gr.Info("📥 Downloading audio layer from YouTube...")
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
    except Exception as e:
        return f"❌ Failed to download video: {str(e)}", ""

    # 2. Transcribe & Summarize
    try:
        gr.Info(f"🎙️ Transcribing locally with Whisper ({whisper_model})...")
        w_model = whisper.load_model(whisper_model)
        result = w_model.transcribe(audio_file)
        transcript = result["text"]
        
        gr.Info(f"🤖 Generating intelligence summary using {llm_model}...")
        prompt = (
            f"You are an expert content analyzer. Summarize the following video transcript into clear, "
            f"structured sections with concise bullet points. Focus on key insights and takeaways:\n\n{transcript}"
        )
        
        response = ollama.chat(model=llm_model, messages=[
            {'role': 'user', 'content': prompt}
        ])
        summary = response['message']['content']
        
        return transcript, summary

    except Exception as e:
        return f"❌ Processing Error: {str(e)}", ""
        
    finally:
        if os.path.exists(audio_file):
            os.remove(audio_file)

# --- Building the Premium Custom Theme UI ---
with gr.Blocks(theme=gr.themes.Soft(primary_hue="purple", secondary_hue="slate")) as demo:
    gr.Markdown(
        """
        # 🎬 Local YouTube Intelligence Terminal
        ### Transcribe and summarize videos with 100% cloud privacy.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ Engine Configurations")
            url_input = gr.Textbox(
                label="YouTube Video Link", 
                placeholder="https://youtube.com..."
            )
            
            with gr.Row():
                whisper_dropdown = gr.Dropdown(
                    choices=["tiny", "base", "small"], 
                    value="base", 
                    label="Whisper Model (Speed vs Accuracy)"
                )
                llm_dropdown = gr.Dropdown(
                    choices=["llama3.1:latest", "llama3.2:3b", "gemma3:270m"], 
                    value="llama3.1:latest", 
                    label="Local LLM Model"
                )
            
            submit_btn = gr.Button("🚀 Generate Summary", variant="primary")
            
        with gr.Column(scale=2):
            with gr.Tab("📝 Summary AI"):
                summary_output = gr.Markdown(value="*Your bulleted AI summary will appear here...*")
            with gr.Tab("📜 Raw Local Transcript"):
                transcript_output = gr.Textbox(
                    label="Extracted Text", 
                    interactive=False, 
                    lines=15
                )

    # Wire up the button action
    submit_btn.click(
        fn=process_video,
        inputs=[url_input, whisper_dropdown, llm_dropdown],
        outputs=[transcript_output, summary_output]
    )

if __name__ == "__main__":
    demo.launch(share=True)
