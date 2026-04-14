import streamlit as st
import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 1. Setup & API Initialization
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

if not os.path.exists("output"):
    os.makedirs("output")

# UI Layout [cite: 30, 31]
st.set_page_config(page_title="Local AI Agent", layout="centered")
st.title("🎙️ Voice-Controlled AI Agent")

# 2. Audio Input Component [cite: 7, 8, 9]
audio_file = st.file_uploader("Upload Audio (.wav or .mp3)", type=["wav", "mp3"])

if audio_file:
    # Save temporary file for processing
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_file.read())

    # 3. STT Logic [cite: 13, 15]
    with st.spinner("Transcribing..."):
        with open("temp_audio.wav", "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=("temp_audio.wav", file.read()),
                model="whisper-large-v3"
            )
        user_input = transcription.text
        st.write(f"**Transcribed:** {user_input}") # [cite: 32]

    # 4. Intent Classification 
    with st.spinner("Analyzing Intent..."):
        system_prompt = """
You are an AI Agent with four specific intents. Respond ONLY in JSON format:

1. CREATE_FILE: For creating empty files. Return {"intent": "CREATE_FILE", "filename": "name.ext"}
2. WRITE_CODE: For generating code. Return {"intent": "WRITE_CODE", "filename": "name.py", "content": "the_actual_code"}
3. SUMMARIZE: For summarizing text. Return {"intent": "SUMMARIZE", "content": "the_summary_text"}
4. CHAT: For general questions. Return {"intent": "CHAT", "content": "your_response"}

Constraint: All code must be functional. All files must have appropriate extensions.
"""
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        result = json.loads(chat_completion.choices[0].message.content)
        intent = result.get("intent")
        st.write(f"**Detected Intent:** {intent}") # [cite: 33]

    # 5. Tool Execution [cite: 24, 25, 27]
    # 5. Tool Execution Logic
    st.divider()
    
    if intent == "CREATE_FILE":
        fname = result.get("filename", "new_file.txt")
        safe_path = os.path.join("output", fname)
        with open(safe_path, "w") as f:
            f.write("") # Just creates an empty file
        st.success(f"✅ Empty file created: {fname}")
        
    

    elif intent == "WRITE_CODE":
        fname = result.get("filename", "script.py")
        code_content = result.get("content", "")
        safe_path = os.path.join("output", fname)
        with open(safe_path, "w") as f:
            f.write(code_content)
        st.success(f"💻 Code written to: {fname}")
        st.code(code_content, language="python") # Previews the code in the UI

    elif intent == "SUMMARIZE":
        summary = result.get("content", "No summary provided.")
        st.info("📝 Summary of your audio:")
        st.write(summary)

    elif intent == "CHAT":
        response = result.get("content", "I'm listening!")
        st.chat_message("assistant").write(response)
        