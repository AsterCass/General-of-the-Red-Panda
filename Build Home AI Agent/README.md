# Build Home AI Agent

English | [中文](README_zh.md)

## Introduction

A home AI agent built with LangChain, LangGraph, and Ollama, supporting intent recognition, tool calling, and RAG retrieval.

### Features

- Intent classification (Chat, Tool, RAG, Web)
- Tool execution with confirmation
- RAG-based knowledge retrieval
- Streaming responses
- Persistent memory with Redis

## Documentation

- [Building a Complete Custom Smart Home System (7) (Agent Chapter - Integrating Large Language Models)](https://www.astercasc.com/article/detail?articleId=AT204218015656262451)
- [Building a Complete Custom Smart Home System (8) (Agent Chapter - Knowledge Base Query)](https://www.astercasc.com/article/detail?articleId=AT204285085250252390)
- [Building a Complete Custom Smart Home System (9) (Agent Chapter - Custom Tool Calling)](https://www.astercasc.com/article/detail?articleId=AT204369538413155532)

## Related Resources

[Download Here](https://pan.baidu.com/s/5P4zJnQ1tJkycI24FEcJC4Q)

## Code

### WSL Related Commands

Manual installation from Microsoft official website: https://learn.microsoft.com/en-us/windows/wsl/install-manual

```shell
# Check current WSL version
wsl -v

# Install WSL framework (if wsl -v does not show a version)
wsl --install

# Switch default WSL version to WSL2
wsl --set-default-version 2

# List installed WSL distributions and their status
wsl --list --verbose

# Completely remove a distribution
wsl --unregister Ubuntu-22.04

# Install a specific distribution
wsl --install Ubuntu-22.04

# Enter a specific distribution
wsl -d Ubuntu-22.04

# Import an external distribution from a file
# (modify the install path and tar file path as needed)
wsl --import Ubuntu-jjdyycm C:\Users\astercasc X:\red.panda\new\jjdyycm.tar

```

### Linux Related (Native Linux or after entering a container using WSL -d <distro>)

todo


### Windows Commands

todo

## Development

If you are not modifying the project, you can skip this section.

* Install [uv](https://docs.astral.sh/uv/) and [Python](https://www.python.org/)

1. Install dependencies:
   ```bash
   uv install
   ```

2. Set up config in `config.toml`:
   - Configure service URLs (Ollama, Redis, Qdrant)
   - Set input/output modes (text/audio)
   - Adjust audio settings (model paths, language, etc.)
   - Specify LLM models and embedding models

3. Run the app:
   ```bash
   uv run app
   ```

## FAQ

### Q: How to switch input/output modes?

**A:** Modify `[input]mode` and `[output]mode` in `config.toml`

### Q: Why is recognition slow?

**A:**

- Check if GPU is enabled (should show `CUDA` instead of `CPU`)
- Reduce `chunk_duration` and `vad_window_sec`
- Use smaller models (turbo versions)

### Q: Why is recognition inaccurate?

**A:**

- Increase `min_silence_ms` to allow more time
- Use larger models (non-turbo versions)
- Increase `min_audio_ms` to filter noise
- Check environmental noise

### Q: Does it support other default languages?

**A:** Modify `[audio]language` in `config.toml`

- `zh` - Chinese
- `en` - English
- More languages see Faster-Whisper documentation

## Tech Stack

- [WSL](https://learn.microsoft.com/en-us/windows/wsl/)
- [LangChain](https://www.langchain.com/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Ollama](https://ollama.ai/)
- [Qdrant](https://qdrant.tech/)
- [Redis](https://redis.io/)
- [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)
- [Qwen3 TTS](https://github.com/andimarafioti/faster-qwen3-tts)
- [Silero VAD](https://github.com/snakers4/silero-vad)
