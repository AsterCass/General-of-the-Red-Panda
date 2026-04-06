# 使用家中旧电脑构建家用人工智能体

[English](README.md) | 中文

## 介绍

演示使用家中旧电脑使用`LLM`为核心，接入自定义的相关`API`以及文档实现`RAG`处理常用需求

* 可以配置某个开灯`localhost:8080/home/api/light/open`然后对话“房间有点暗”即可自动开灯
* 可以配置文档中心，存入相关内容，当你询问文档中的问题的时候，自动回复相应答案
* 可以自动开启联网搜索，回答文档中心和模型自带中没有的知识，比如“最新的一联的世界杯的冠军是谁”


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




## 技术栈


- [WSL官网](https://learn.microsoft.com/en-us/windows/wsl/)