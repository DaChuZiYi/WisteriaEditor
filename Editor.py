# 导入模块
import importlib.util
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText #滚动文本框
from ttkbootstrap.constants import *
import os

# 程序所在目录
current_directory = os.path.dirname(os.path.abspath(__file__))

root = ttk.Window(
    title="紫藤编辑器",  # 设置窗口的标题
    themename="minty",  # 设置主题
    size=(700, 600),  # 窗口的大小
    position=(100, 100),  # 窗口所在的位置
    minsize=(500, 500),  # 窗口的最小宽高
    maxsize=(1920,1080),    #窗口的最大宽高
    resizable=(True,True),  # 设置窗口是否可以更改大小
    alpha=1.0,  # 设置窗口的透明度(0.0完全透明）
)

menubar = ttk.Menu(root)
