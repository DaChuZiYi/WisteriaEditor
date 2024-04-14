# 导入模块
import importlib.util
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText  # 滚动文本框
from ttkbootstrap.constants import *
import os
import yaml
import requests
from bs4 import BeautifulSoup
import subprocess
import time
# 程序所在目录
current_directory = os.path.dirname(os.path.abspath(__file__))
current_name = "WisteriaEditor"


# 读取配置
def load_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data


# 加载配置
config_data = load_yaml(os.path.join(current_directory, "Data\\config.yaml"))

# 自动更新
if config_data["autoupdate"]:
    url = "https://dachuziyi.github.io/update"
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"加载失败: {response.status_code}")
        exit(1)

    soup = BeautifulSoup(html_content, "html.parser")

    # 获取
    dl = soup.find("dl")

    # 遍历
    for dt, dd in zip(dl.find_all("dt"), dl.find_all("dd")):
        term = dt.text.strip()
        version = dd.text.strip()
        if current_name == term and version != config_data["version"]:
            print(f"发现新版本 {version}，当前版本为 {config_data['version']}")
            # 下载新版本
            if input("是否现在更新?(Y/n)") != "n":
                print("正在启动更新程序,本程序将关闭")
                time.sleep(5)
                update_exe_path = f"{current_directory}\\Update\\update.exe"
                new_window_flags = subprocess.CREATE_NEW_CONSOLE  # 启动新窗口标志（Windows）
                subprocess.Popen([update_exe_path], creationflags=new_window_flags)
        else:
            print(f"{term} 已是最新版本")
            break


root = ttk.Window(
    title="紫藤编辑器",  # 设置窗口的标题
    themename="minty",  # 设置主题
    size=(700, 600),  # 窗口的大小
    position=(100, 100),  # 窗口所在的位置
    minsize=(500, 500),  # 窗口的最小宽高
    maxsize=(1920, 1080),  # 窗口的最大宽高
    resizable=(True, True),  # 设置窗口是否可以更改大小
    alpha=1.0,  # 设置窗口的透明度(0.0完全透明）
)

menubar = ttk.Menu(root)
