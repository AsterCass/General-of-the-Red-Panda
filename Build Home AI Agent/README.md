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



### Windows Commands


## Development

If you are not modifying the project, you can skip this section.

* Install [uv](https://docs.astral.sh/uv/) and [Python](https://www.python.org/)

1. Install dependencies:
   ```bash
   uv install
   ```

2. Set up environment variables in `.env`:
   ```
   QDRANT_URL=http://localhost:6333
   OLLAMA_BASE_URL=http://localhost:11434
   REDIS_URL=redis://localhost:6379
   MODEL_NAME=qwen2.5:7b
   MODEL_NAME_LIGHT=qwen2.5:1.5b
   EMBED_TEXT_MODEL_NAME=bge-m3
   RESET_COLLECTIONS=false
   ```

3. Run the app:
   ```bash
   uv run app
   ```


## Tech Stack

- [WSL](https://learn.microsoft.com/en-us/windows/wsl/)