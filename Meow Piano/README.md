# Meow Piano

English | [中文](README_zh.md)

## Introduction

A desktop utility tool.

Do you sometimes feel that working or studying on your computer is a bit boring? Meow Piano is here to help!
When you type on your keyboard, the program will automatically play corresponding piano sounds and display animated rhythm waves around the edges of your screen.

You can disable either the sound or the visual effects if you prefer. Even when the program is minimized and running in the background, it will continue to work normally.

Future updates may introduce rhythm upgrades, such as special sound and visual effects when typing very fast or when typing specific configured key sequences.

### Screenshots

<img src="img/1.jpg" width="500"/>

<img src="img/2.jpg" width="500"/>


## Documentation

More detailed documentation and extended content can be found here:
* [Click here](https://www.astercasc.com/article/detail?articleId=AT202776160889761382)
* [Click here](https://www.astercasc.com/article/detail?articleId=AT202946490116003020)

If you have any questions, you can also leave a comment at the bottom of the pages above.


## Download

Download links for the main program (choose one depending on your needs):

Baidu Netdisk: [Click here](https://pan.baidu.com/s/5P4zJnQ1tJkycI24FEcJC4Q)

GitHub Releases: [Click here](https://github.com/AsterCass/General-of-the-Red-Panda/releases)


## Development

If you are not planning to modify or develop the project, you can skip this section.

* Install [uv](https://docs.astral.sh/uv/) and [Python](https://www.python.org/)

```shell
# Run
uv run app
# Build
uv run pyinstaller --onefile --noconsole --icon=assets/logo.ico --name 喵喵律动 --add-data "assets;assets"  src/meow_piano/__main__.py
# Refresh dependencies
uv lock --no-cache
uv sync
```

