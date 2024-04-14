import os
import requests
from bs4 import BeautifulSoup
import tempfile
import zipfile
import shutil
import yaml

def unzip_file(zip_path, destination_dir):
    """
    解压ZIP文件到指定目录。

    参数:
    zip_path (str): ZIP文件的路径。
    destination_dir (str): 目标解压目录的路径。
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(destination_dir)
    

current_directory = os.path.dirname(os.path.abspath(__file__))
# version = "0.0.1"

print(current_directory)
url = "https://dachuziyi.github.io/update"
response = requests.get(url)
if response.status_code == 200:
    html_content = response.text
else:
    print(f"获取版本信息时加载失败: {response.status_code}")
    exit(1)
soup = BeautifulSoup(html_content, "html.parser")
dl = soup.find("dl")
for dt, dd in zip(dl.find_all("dt"), dl.find_all("dd")):
        term = dt.text.strip()
        version = dd.text.strip()
        if "WisteriaEditor" == term:
            break
else: print("无法找到版本信息") ; exit(1)

url_list = [
    f"https://github.com/DaChuZiYi/WisteriaEditor/archive/refs/tags/{version}.zip",
    f"https://codeload.github.com/DaChuZiYi/WisteriaEditor/zip/refs/tags/{version}",
    f"https://mirror.ghproxy.com/https://github.com/DaChuZiYi/WisteriaEditor/archive/refs/tags/{version}.zip"
]
print("请选择下载链接(输入序号)：\n>===第一项为GitHub源")
for i,j in zip(range(len(url_list)),url_list):print(f"{i+1}. {j}")
temp_dir = tempfile.mkdtemp(prefix="temp_", dir=current_directory)
target_path = os.path.join(temp_dir, f"{version}.zip")
download = requests.get(url_list[int(input(">"))-1], stream=True)
with open(target_path, "wb") as f:
    for chunk in download.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
print("已结束下载\n正在解压中\n")
unzip_file(target_path, os.path.join(current_directory,"Temp"))

print("解压完成\n正在安装更新\n")
os.rmdir(temp_dir)

# 定位新版本主程序
temp_version_dir = os.path.join(current_directory, "Temp", f"WisteriaEditor-{version}")
editor_exe_in_temp = None

for file in os.listdir(temp_version_dir):
    if file.lower() == "editor.exe":  # 考虑大小写不敏感
        editor_exe_in_temp = os.path.join(temp_version_dir, file)
        print("正在替换主程序")
        break
if editor_exe_in_temp is None:
    print("未在新版本目录中找到Editor.exe")
else:
    # 计算目标路径（current_directory的上一级目录）
    parent_dir = os.path.dirname(os.path.abspath(current_directory))
    target_editor_exe = os.path.join(parent_dir, "Editor.exe")

    # 执行替换操作
    try:
        shutil.move(editor_exe_in_temp, target_editor_exe)
        print("成功替换到上级目录的Editor.exe")
    except Exception as e:
        print(f"替换失败: {e}")

os.remove(os.path.join(temp_version_dir,"LICENSE"))

print("正在更新配置")

if input("是否替换旧配置(Y/n)\n注意:不替换则为更新配置\n这会删除所有注释,并且可能会有配置产生错误").lower() == "n":
    for file in os.listdir(os.path.join(temp_version_dir,"Data")):
        if file.lower() == "config.yaml":
            def load_yaml(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    data = yaml.safe_load(file)
                return data
            def merge_dicts(base_dict, update_dict):
                for key, value in update_dict.items():
                    if key not in base_dict or key == "version":
                        base_dict[key] = value

            new_config_data = load_yaml(os.path.join(temp_version_dir, "Data\\config.yaml"))
            old_config_data = load_yaml(os.path.join(os.path.dirname(current_directory), "Data\\config.yaml"))

            merge_dicts(old_config_data, new_config_data)
            
    def save_yaml(data, output_path):
        with open(output_path, "w", encoding="utf-8") as file:
            yaml.safe_dump(data, file, sort_keys=False)

    output_path = os.path.join(os.path.dirname(current_directory), "Data\\config.yaml")
    save_yaml(old_config_data, output_path)
    
    os.rmdir(os.path.join(temp_version_dir,"Data"))

for file in os.listdir(temp_version_dir):
    shutil.move(os.path.join(temp_version_dir, file),os.path.dirname(current_directory))

os.rmdir(temp_version_dir)

print("更新完成")
