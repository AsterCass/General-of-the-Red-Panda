# 喵喵律动

[English](README.md) | 中文

## 介绍

一个桌面工具

是否感觉平时使用电脑工作、学习太无聊。【喵喵律动】启动！在你输入打字的时候，会自动发出相应的钢琴声音，以及屏幕四周出现跳动音律，当然你可以选择关掉他们中的任何一个，即使在程序最小化在后台也能正常工作

后续迭代可能会考虑加入韵律升格，即打字速度过快或打出配置字符顺序，声音以及屏幕音律出现特殊效果


### 截图

<img src="img/1.jpg" width="500"/>

<img src="img/2.jpg" width="500"/>


## 具体文档

具体文档以及相关拓展更多内容可以访问：[点击此处](https://www.astercasc.com/article/detail?articleId=AT202776160889761382)

如果有任何问题也可在该链接网址的最下方留言

## 软件下载

默认环境下所需的模型文件以及主程序的下载（提供给不同需求用户，选择其一即可）：

玛丽亚内居民：[点击此处](https://pan.baidu.com/s/5P4zJnQ1tJkycI24FEcJC4Q)

调查兵团：[点击此处](https://github.com/AsterCass/General-of-the-Red-Panda/releases)

## 开发

不进行开发修改的小伙伴略过这个部分

1. 安装[uv](https://docs.astral.sh/uv/)以及[python](https://www.python.org/)环境

```shell
# 安装运行
uv run app
# 打包
uv run pyinstaller --onefile --noconsole --icon=assets/logo.ico --name 喵喵律动 --add-data "assets;assets"  src/meow_piano/__main__.py
# 清理修改依赖
uv lock --no-cache
uv sync
```


## 技术栈

