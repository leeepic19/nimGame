# Nim 汉堡游戏

## 项目简介
这是一个基于 Tkinter 的 Nim 汉堡棋游戏，支持人机对战，带有丰富的图片和音效资源。

## 目录结构
```
ai_easy.pkl  ai_hard.pkl  ai_medium.pkl
nim_gui.py   nim.py   nimplay.py
requirements.txt
music/      picture/
```

## 依赖安装
```bash
pip install -r requirements.txt
```

## 运行方法
```bash
python nim_gui.py
```

## 打包为可执行文件（macOS）
```bash
pip install pyinstaller
pyinstaller --onefile --add-data "music:music" --add-data "picture:picture" nim_gui.py
```
打包后 dist/nim_gui 可直接运行。

## 资源说明
- music/ 目录下为所有音效文件
- picture/ 目录下为所有图片资源
- ai_easy.pkl、ai_medium.pkl、ai_hard.pkl 为AI模型

## 注意事项
- 运行或打包时 music/ 和 picture/ 需与主程序同级
- 如需 Windows 打包，请在 Windows 下用分号分隔资源路径

## 联系方式
如有问题欢迎反馈。
