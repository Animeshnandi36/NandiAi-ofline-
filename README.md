# Nandi Ai — Offline Generative AI Chat Assistant

A fully offline, local-only generative AI chat assistant built with Streamlit, LangChain and Ollama (LLaMA 2 7B). Designed for air-gapped or sensitive environments that prohibit external network calls.

## Key Features
- 100% offline operation (local LLM inference)
- Session-isolated conversations (per-tab session ID)
- Context window management (trim beyond last 10 messages)
- Streaming response support for better UX
- Security-first defaults (no cloud APIs required)

## Project Structure
.
├── app.py
├── backend.py
├── requirements.txt
├── README.md
├── .gitignore
└── .github/
    └── workflows/ci.yml

## Requirements
- Python 3.9+
- Ollama installed and a local LLaMA2:7b model available
- Install Python deps: pip install -r requirements.txt

## Run locally
1. Install Ollama (https://ollama.com) and pull the model:
   ```bash
   ollama pull llama2:7b
   ```
2. Install Python deps:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   streamlit run app.py
   ```

## Notes & Troubleshooting
- If imports from `langchain_core` or `langchain_ollama` fail, check package names and versions; package naming changed across LangChain releases.
- This project is a demo for offline LLM use — review and pin dependency versions before production.
