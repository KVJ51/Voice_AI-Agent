# 🎙️ Voice-Controlled Local AI Agent

A robust, voice-activated AI agent capable of local file operations, code generation, and text summarization through a clean Streamlit interface.

## 🚀 Overview
This project bridges the gap between spoken commands and local system actions. It uses a hybrid architecture that offloads heavy inference to the cloud to maintain high performance on standard hardware (8GB RAM), while executing sensitive file operations locally.

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Speech-to-Text (STT):** Groq (Whisper-large-v3)
- **Intent Engine:** Groq (Llama-3.1-70b-versatile)
- **Orchestration:** Python (OS, JSON, Dotenv)

## 🏗️ Architecture & Decisions
### Why API-based Inference?
While the system is designed to be a "Local Agent," the primary inference (STT and LLM) is handled via the Groq API. 
**Decision Factor:** On a machine with **8GB of RAM**, running a quantized Llama-3 and Whisper locally caused significant latency and system lag. By using Groq's LPU (Language Processing Units), we achieved:
- Sub-second transcription and intent detection.
- Zero system lag during model loading.
- High accuracy using a 70B parameter model that wouldn't fit in local VRAM.

## 🔒 Safety Constraints
As per the assignment requirements:
- **Restricted Access:** All file creation and code writing are strictly confined to the `/output` folder.
- **Path Sanitization:** The agent uses `os.path.join` to prevent directory traversal or accidental system overwrites.

## 📋 Setup Instructions
1. **Clone the Repo:**
   ```bash
   git clone <your-repo-link>
   cd voice-ai-agent

2.**Environment Variables:**
Create a .env file and add your Groq API Key:
GROQ_API_KEY=your_actual_key

3.**Install Dependencies:**
pip install -r requirements.txt

4.**Run the App:**
streamlit run main.py