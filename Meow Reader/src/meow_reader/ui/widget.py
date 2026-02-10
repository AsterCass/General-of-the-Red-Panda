import tkinter as tk
from tkinter import messagebox

class MainWidget:
    def __init__(self, root):
        self.root = root
        root.title("喵喵朗读")
        root.geometry("600x300")

        # 标签
        tk.Label(root, text="请输入你的名字：", font=("Microsoft YaHei", 12)).pack(pady=10)

        # 输入框
        self.entry = tk.Entry(root, width=30, font=("Microsoft YaHei", 12))
        self.entry.pack(pady=5)

        # 按钮
        tk.Button(
            root,
            text="提交",
            width=10,
            command=self.on_submit,
            bg="#4CAF50",
            fg="white"
        ).pack(pady=20)

        # 多行文本显示区
        self.result = tk.Text(root, height=5, width=40, font=("Microsoft YaHei", 11))
        self.result.pack(pady=10)

    def on_submit(self):
        name = self.entry.get().strip()
        if name:
            self.result.delete(1.0, tk.END)
            self.result.insert(tk.END, f"你好，{name}！\n欢迎使用 Tkinter。")
        else:
            messagebox.showwarning("提示", "请输入名字哦～")