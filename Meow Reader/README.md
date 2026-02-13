# Meow Reader

English | [中文](README_zh.md)

## Introduction

Meow Reader

A simple desktop utility tool.

It automatically reads English text from your clipboard, translates it into Chinese, and plays the English pronunciation (other languages are also supported by replacing the models).

If you feel that:

When browsing English websites or reading documents,
you often need to copy → switch to a translator → check the meaning → click the pronunciation,
and the back-and-forth interrupts your reading flow,

you can try this tool to assist your daily reading and comprehension.

Future updates may adjust features based on usage experience,
or support additional languages (for example, allowing you to switch the target translation language directly in the UI).

The current translation and TTS models are chosen as a balance between resource usage, file size, and quality.
If your machine has better performance and you don’t mind larger storage usage, you can try models such as:

* [TranslateGemma](https://huggingface.co/google/translategemma-4b-it)
* [HY-MT](https://github.com/Tencent-Hunyuan/HY-MT)
* Or other models

## Documentation

For detailed documentation and extended information, please visit:
[Click here](https://www.astercasc.com/article/detail?articleId=AT196496468516617011)

This article describes an earlier version that used a translation API + pyttsx3.
The current version is fully offline, but the core idea remains the same.

If you have any questions, you can leave a comment at the bottom of that page.

## Download

Download links for the main program and required model files (choose one depending on your needs):

Baidu Netdisk: [Click here](https://pan.baidu.com/s/5P4zJnQ1tJkycI24FEcJC4Q)

GitHub Releases: [Click here](https://github.com/AsterCass/General-of-the-Red-Panda/releases)

### Optional Configuration

You can create a `config.toml` file in the program root directory to replace the translation model, TTS model, or dictionary path
(only do this if you know what you are doing — source code modifications may be required).

```toml
[path]
transModelPath="models/opus-mt-en-zh"
speakModelPath="models/en_US-lessac-medium/en_US-lessac-medium.onnx"
dictDbPath="models/dict/ecdict.db"
```

## Development

If you are not modifying the project, you can skip this section.

* Install [uv](https://docs.astral.sh/uv/) and [Python](https://www.python.org/)
* Copy the models folder from the download package into the project root directory

```shell
# Run
uv run app
# Build
uv run pyinstaller --onefile --noconsole --icon=assets/logo.ico --name 喵喵朗读 --collect-all piper --add-data "assets;assets"  src/meow_reader/__main__.py
# Refresh dependencies
uv lock --no-cache
uv sync
```


## Tech Stack

- [Piper](https://github.com/OHF-Voice/piper1-gpl)
- [Helsinki-NLP](https://www.modelscope.cn/organization/Helsinki-NLP?tab=model)
- [ECDICT](https://github.com/skywind3000/ECDICT)