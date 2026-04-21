# 使用家中旧电脑构建家用人工智能体

[English](README.md) | 中文

## 介绍

一个基于 LangChain、LangGraph 和 Ollama 构建的家用人工智能体，支持正常聊天、工具调用和文档检索等功能

## 功能

- 意图分类（Chat、Tool、RAG、Web）
- 工具执行并确认
- 基于 RAG 的知识检索
- 流式响应
- 使用 Redis 的持久化记忆
- 支持文本和语音输入输出
- 实时语音识别（Faster-Whisper + Silero VAD）
- 语音合成（Qwen3 TTS）

## 项目结构

```
Build Home AI Agent/
├── config.toml              # 配置文件
├── pyproject.toml           # 项目依赖
├── src/meow_ai_agent/       # 主要代码
│   ├── __main__.py          # 程序入口
│   ├── audio/               # 音频处理
│   │   ├── input.py         # 语音输入
│   │   └── output.py        # 语音输出
│   ├── config/              # 配置
│   ├── constants/           # 常量和枚举
│   ├── model/               # AI 模型逻辑
│   │   ├── app.py           # LangGraph 应用
│   │   ├── base.py          # 基础模型配置
│   │   ├── intent.py        # 意图分类
│   │   ├── rag.py           # RAG 检索
│   │   └── tools.py         # 工具调用
│   └── utils/               # 工具函数
├── models/                  # 本地模型文件
├── data/                    # 数据存储
└── tests/                   # 测试
```

## 具体文档

- [构建完全自定义的全屋智能系统（七）（智能体篇-接入大语言模型）](https://www.astercasc.com/article/detail?articleId=AT204218015656262451)
- [构建完全自定义的全屋智能系统（八）（智能体篇-知识库查询）](https://www.astercasc.com/article/detail?articleId=AT204285085250252390)
- [构建完全自定义的全屋智能系统（九）（智能体篇-自定义工具调用）](https://www.astercasc.com/article/detail?articleId=AT204369538413155532)

## 相关资源下载地址

[点击此处](https://pan.baidu.com/s/5P4zJnQ1tJkycI24FEcJC4Q)

## 代码

### WSL相关内容

微软官网手动安装WSL：[点击此处](https://learn.microsoft.com/zh-cn/windows/wsl/install-manual)

```shell
# 查看当前WSL版本
wsl -v
# 安装WSL框架（如果你电脑使用 wsl -v 无法看到版本号的话）
wsl --install
# 切换到WSL2版本
wsl --set-default-version 2
# 查看当前宿主机已经安装WSL镜像容器以及状态
wsl --list --verbose
# 彻底删除某个容器
wsl --unregister Ubuntu-22.04
# 安装某个镜像容器
wsl --install Ubuntu-22.04
# 进入某个容器
wsl -d Ubuntu-22.04
# 指定文件安装外部镜像容器（修改安装地址和打包文件所在地址）
wsl --import Ubuntu-jjdyycm C:\Users\astercasc X:\red.panda\new\jjdyycm.tar
```

### Linux 相关（即你使用的是原生Linux或者已经使用【WSL -d 指定容器名】进入容器）


英伟达显卡容器支持：

```shell
curl -fsSL https://mirrors.ustc.edu.cn/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://mirrors.ustc.edu.cn/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
systemctl restart docker
```

相关服务安装：

```shell
# Docker 安装相关镜像
# Ollama
# 标记映射文件夹
mkdir  -p /home/service/ollama/data
# 容器配置
cd /home/service/ollama
cat <<'EOF' > /home/service/ollama/docker-compose.yml
services:
  ollama:
    image: ollama/ollama
    container_name: ollama
    restart: always
    ports:
      - "11434:11434"
    volumes:
      - /home/service/ollama/data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - OLLAMA_FLASH_ATTENTION=1
EOF
docker compose up -d

# 这里根据你的硬件配置拉取合适的镜像，如果不清楚可以先拉取小模型测试，确认没问题后再拉取大模型
docker exec ollama ollama pull qwen3:14b-q4_K_M

# Redis
# 标记映射文件夹
mkdir  -p /home/service/redis/data
# 容器配置
cd /home/service/redis
cat <<'EOF' > /home/service/redis/docker-compose.yml
services:
  redis:
    image: redis/redis-stack:latest
    container_name: redis
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - /home/service/redis/data:/data
EOF
docker compose up -d

# Qdrant
# 标记映射文件夹
mkdir  -p /home/service/qdrant/data
# 容器配置
cd /home/service/qdrant
cat <<'EOF' > /home/service/qdrant/docker-compose.yml
services:
  qdrant:
    image: qdrant/qdrant
    container_name: qdrant
    restart: always
    ports:
      - "6333:6333"
    volumes:
      - /home/service/qdrant/data:/qdrant/storage
EOF
docker compose up -d
```

### Windows相关命令

todo

## 开发

不进行开发修改的小伙伴略过这个部分

* 安装[uv](https://docs.astral.sh/uv/)以及[python](https://www.python.org/)环境

1. 安装相应服务端并配置地址在`config.toml`中，如 Ollama、Redis、RAG向量数据库等，参考上方**具体文档**部分

2. 安装依赖:
   ```bash
   uv install
   ```

3. 设置配置，在`config.toml`中：
   - 配置服务地址（Ollama、Redis、Qdrant）
   - 设置输入输出模式（文本/语音）
   - 调整音频设置（模型路径、语言等）
   - 指定LLM模型和嵌入模型

4. 运行:
   ```bash
   uv run app
   ```

## 常见问题

### Q: 如何切换输入/输出模式？

**A:** 修改 `config.toml` 中的 `[input]mode` 以及 `[output]mode`

### Q: 为什么识别很慢？

**A:**

- 检查是否启用了GPU（应显示 `CUDA` 而不是 `CPU`）
- 减小 `chunk_duration` 和 `vad_window_sec`
- 使用更小的模型（turbo版本）

### Q: 为什么识别不准确？

**A:**

- 增加 `min_silence_ms` 给更多时间
- 使用更大的模型（non-turbo版本）
- 增加 `min_audio_ms` 过滤噪音
- 检查环境噪音

### Q: 支持其他默认语言吗？

**A:** 修改`config.toml` 中的 `[audio]language`

- `zh` - 中文
- `en` - 英文
- 更多语言见 Faster-Whisper 文档


## 技术栈

- [WSL](https://learn.microsoft.com/en-us/windows/wsl/)
- [LangChain](https://www.langchain.com/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Ollama](https://ollama.ai/)
- [Qdrant](https://qdrant.tech/)
- [Redis](https://redis.io/)
- [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)
- [Qwen3 TTS](https://github.com/andimarafioti/faster-qwen3-tts)
- [Silero VAD](https://github.com/snakers4/silero-vad)
