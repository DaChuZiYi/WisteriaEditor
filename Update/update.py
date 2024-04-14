
current_directory = input()
version = input()


params = [current_directory,version]

# 调用 b.exe 并传递参数
result = subprocess.run(['path/to/b.exe'] + params, capture_output=True, text=True)

# 检查返回状态码及输出
if result.returncode == 0:
    print("b.exe ran successfully")
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)
else:
    print("b.exe failed with exit code:", result.returncode)