# 喵喵朗读

[English](README.md) | 中文

## 介绍



## 具体文档

具体文档以及相关拓展更多内容可以访问：[点击此处](https://www.astercasc.com/article/detail?articleId=AT196496468516617011)

该文档为稍早版本，使用翻译 API + pyttsx3 实现，和目前的完全离线版本稍有不同，但是核心本质都是一样的

如果有任何问题也可在该链接网址的最下方留言

## 下载

[点击此处](https://pan.baidu.com/s/5P4zJnQ1tJkycI24FEcJC4Q)

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