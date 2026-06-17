# Nandi Ai — Offline Generative AI Chat Assistant

A fully offline, local-only generative AI chat assistant built with Streamlit, LangChain and Ollama (LLaMA 2 7B). Designed for air-gapped or sensitive environments that prohibit external network calls.

## Key Features
- 100% offline operation (local LLM inference)
- Session-isolated conversations (per-tab session ID)
- Context window management (trim beyond last 10 messages)
- Streaming response support for better UX
- Security-first defaults (no cloud APIs required)
- Persistent conversation history per session

## Project Structure
```
.
├── app.py                 # Streamlit frontend application
├── backend.py             # LLM backend with LangChain integration
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
└── .gitignore             # Git ignore configuration
```

## Requirements
- **Python 3.9+**
- **Ollama** (download from https://ollama.com)
- **LLaMA 2 7B model** (pulled via Ollama)
- Internet connection (only for initial setup; app runs fully offline)

## Installation & Setup

### Step 1: Install Ollama
Download and install Ollama from [https://ollama.com](https://ollama.com)

### Step 2: Pull the LLaMA 2 Model
Open your terminal and run:
```bash
ollama pull llama2:7b
```

### Step 3: Install Python Dependencies
Clone or download this repository, then install the required Python packages:
```bash
pip install -r requirements.txt
```

## How to Run

### Option 1: Standard Run
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Option 2: Run with Custom Port
```bash
streamlit run app.py --server.port 8502
```

### Option 3: Run with Specific Host
```bash
streamlit run app.py --server.address 127.0.0.1
```

### Option 4: Production Mode
```bash
streamlit run app.py --logger.level=error --client.showErrorDetails=false
```

## Usage

1. **Open the Application**: Navigate to `http://localhost:8501` in your browser
2. **Chat**: Type your query in the chat input field and press Enter
3. **View History**: All conversation history is displayed in the chat window
4. **Clear Context**: Click "Clear Context Window" button in the sidebar to reset the conversation
5. **Monitor Status**: Check the sidebar for connection and encryption status

## Architecture

### Frontend (app.py)
- Built with **Streamlit** for interactive UI
- Manages session state and chat history
- Streams responses in real-time
- Secure error handling

### Backend (backend.py)
- Integrates **LangChain** for prompt management
- Uses **ChatOllama** for local LLM inference
- Maintains in-memory conversation history
- Provides streaming response generation

### Flow
1. User input → Frontend (Streamlit)
2. Session management & history tracking
3. LLM inference via Ollama (local, offline)
4. Streaming response back to user
5. History persistence per session

## Configuration

### Default Settings
- **Model**: `llama2:7b`
- **Temperature**: 0.3 (more deterministic responses)
- **Max History**: Last 10 messages per session
- **Ollama Endpoint**: `localhost:11434` (default)

### Customization
Edit `backend.py` to modify:
- Model name (line 36): `llm = ChatOllama(model="llama2:7b")`
- Temperature (line 36): `temperature=0.3`
- System prompt (line 42): Update the system message
- History limit (line 28): Adjust `> 10` to your preference

## Troubleshooting

### Issue: "Failed to connect to Ollama"
**Solution**: 
- Ensure Ollama is running: `ollama serve` in a terminal
- Check Ollama is listening on `localhost:11434`

### Issue: "LangChain imports failed"
**Solution**:
- Reinstall dependencies: `pip install --upgrade -r requirements.txt`
- Ensure compatible versions are installed

### Issue: "llama2:7b model not found"
**Solution**:
- Pull the model: `ollama pull llama2:7b`
- Verify with: `ollama list`

### Issue: Application runs slowly
**Solution**:
- First run will be slower as the model loads
- Ensure sufficient RAM (minimum 8GB recommended for llama2:7b)
- CPU inference may be slower; GPU acceleration via Ollama is recommended

### Issue: Chat history not persisting
**Solution**:
- Session history is in-memory; it resets on app restart
- This is by design for privacy
- To persist, modify `backend.py` to use a database instead

## Notes & Best Practices

- **Privacy**: All data stays local. No cloud transmission occurs.
- **Production**: Review and pin dependency versions before using in production
- **Dependencies**: Package names in LangChain have changed; if imports fail, check versions
- **Memory**: Each session maintains up to 10 messages in memory
- **Model Options**: You can replace `llama2:7b` with other Ollama models (e.g., `mistral`, `neural-chat`)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Support & Issues

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify Ollama is running and the model is pulled
3. Check Python and dependency versions match requirements
4. Review error messages in the Streamlit terminal

## Contributing

Feel free to fork this project and submit improvements!

---

**Version**: 1.0  
**Last Updated**: June 2026
