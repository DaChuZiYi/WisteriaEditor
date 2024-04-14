@echo off

REM 从命令行参数中提取tag和current_directory的值
set tag=%~1
set current_directory=%~2
set tag=0.0.1
set current_directory=c:\Users\Administrator\Desktop\WisteriaEditor

REM 继续原来的.bat文件内容，使用%tag%和%current_directory%
set DOWNLOAD_URL=https://codeload.github.com/DaChuZiYi/WisteriaEditor/zip/refs/tags/%tag%.zip
set DOWNLOAD_PATH=C:\Temp\update.zip
set EXTRACT_PATH=%current_directory%

bitsadmin /transfer UpdateDownload /priority normal /download /retryTimeout:60 /dynamic /notifycmdline:C:\Temp\download_complete.bat "%DOWNLOAD_URL%" "%DOWNLOAD_PATH%"

REM 检查携带版7-Zip是否存在，如果不存在则下载
set PORTABLE_7ZIP_DOWNLOAD_URL=https://download2.portableapps.com/portableapps/7-ZipPortable/7-ZipPortable_23.01.paf.exe
set PORTABLE_7ZIP_EXE="%current_directory%\current"

if not exist "%PORTABLE_7ZIP_EXE%" (
    bitsadmin /transfer DownloadPortable7Zip /priority high /download /retryTimeout:600 /dynamic "%PORTABLE_7ZIP_DOWNLOAD_URL%" "%PORTABLE_7ZIP_EXE%""%PORTABLE_7ZIP_DOWNLOAD_URL%" "%PORTABLE_7ZIP_EXE%"
    if not exist "%PORTABLE_7ZIP_EXE%" (
        echo Failed to download portable 7-Zip.
        goto :EOF
    )
)

REM 设置PATH包含携带版7-Zip路径
set "PATH=%PATH%;%CD%\Temp"

set "PATH=%PATH%;C:\Program Files\7-Zip"

if exist "%DOWNLOAD_PATH%" (
    echo Downloaded successfully. Extracting...
    7z x "%DOWNLOAD_PATH%" -o"%EXTRACT_PATH%" -aoa
    if %ERRORLEVEL% equ 0 (
        echo 提取完成。
        start "" "%EXTRACT_PATH%\update.exe"
        rem 进行其他更新后操作，如替换旧文件、重启服务等
    ) else (
        echo 提取失败。
    )
) else (
    echo 下载失败
)
