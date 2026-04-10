# 使用家中旧电脑构建家用人工智能体

[English](README.md) | 中文

## 介绍

一个基于 LangChain、LangGraph 和 Ollama 构建的家用 AI 代理，支持意图识别、工具调用和 RAG 检索

### 功能

- 意图分类（Chat、Tool、RAG、Web）
- 工具执行并确认
- 基于 RAG 的知识检索
- 流式响应
- 使用 Redis 的持久化记忆

## 具体文档



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


### Windows相关命令


## 开发

不进行开发修改的小伙伴略过这个部分

* 安装[uv](https://docs.astral.sh/uv/)以及[python](https://www.python.org/)环境

1. 安装依赖:
   ```bash
   uv install
   ```

2. 设置环境，在`.env`中：
   ```
   QDRANT_URL=http://localhost:6333
   OLLAMA_BASE_URL=http://localhost:11434
   REDIS_URL=redis://localhost:6379
   MODEL_NAME=qwen2.5:7b
   MODEL_NAME_LIGHT=qwen2.5:1.5b
   EMBED_TEXT_MODEL_NAME=bge-m3
   RESET_COLLECTIONS=false
   ```

3. 运行:
   ```bash
   uv run app
   ```


## 技术栈

- [WSL官网](https://learn.microsoft.com/en-us/windows/wsl/)