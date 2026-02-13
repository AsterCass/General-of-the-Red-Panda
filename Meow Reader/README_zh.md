# 喵喵朗读

[English](README.md) | 中文

## 介绍

喵喵朗读

一个简单的桌面小工具

它会自动读取剪贴板中的英文内容，翻译成中文，并播放英文发音（其他语言也可以，替换模型即可）

如果你觉得：
在浏览英文网页、看资料或文档时，
经常需要复制 -> 切换翻译软件 -> 查意思 -> 点发音，
来回操作有点打断节奏

可以尝试这个软件辅助日常阅读时候的理解

后续可能会根据使用体验慢慢调整功能，或者适配其他语言（比如支持直接在UI界面中切换目标翻译语言）

目前的翻译模型以及朗读模型是中和衡量资源占用和文件大小以及效果，
如果你的机器性能比较好，也不在意占用更大存储空间，可以使用[TranslateGemma](https://huggingface.co/google/translategemma-4b-it)或者[HY-MT](https://github.com/Tencent-Hunyuan/HY-MT)或者[]()等等模型

## 具体文档

具体文档以及相关拓展更多内容可以访问：[点击此处](https://www.astercasc.com/article/detail?articleId=AT196496468516617011)

该文档为稍早版本，使用翻译 API + pyttsx3 实现，和目前的完全离线版本稍有不同，但是核心本质都是一样的

如果有任何问题也可在该链接网址的最下方留言

## 软件下载

默认环境下所需的模型文件以及主程序的下载（提供给不同需求用户，选择其一即可）：

玛丽亚内居民：[点击此处](https://pan.baidu.com/s/5P4zJnQ1tJkycI24FEcJC4Q)

调查兵团：[点击此处](https://github.com/AsterCass/General-of-the-Red-Panda/releases)

### 额外的

你可以在程序根目录下创建`config.toml`写入内容，替换使用的模型以及字典目录（前提是你知道自己在干什么，必要的时候需要修改源代码）

```toml
[path]
transModelPath="models/opus-mt-en-zh"
speakModelPath="models/en_US-lessac-medium/en_US-lessac-medium.onnx"
dictDbPath="models/dict/ecdict.db"
```

## 开发

不进行开发修改的小伙伴略过这个部分

1. 安装[uv](https://docs.astral.sh/uv/)以及[python](https://www.python.org/)环境
2. 将上方【下载】的内容中的 models 文件夹复制到项目根目录下

```shell
# 安装运行
uv run app
# 打包
uv run pyinstaller --onefile --noconsole --icon=assets/logo.ico --name 喵喵朗读 --collect-all piper --add-data "assets;assets"  src/meow_reader/__main__.py
# 清理修改依赖
uv lock --no-cache
uv sync
```


## 技术栈

- [Piper](https://github.com/OHF-Voice/piper1-gpl)
- [Helsinki-NLP](https://www.modelscope.cn/organization/Helsinki-NLP?tab=model)
- [ECDICT](https://github.com/skywind3000/ECDICT)