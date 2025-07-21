@echo off
setlocal

:: --- Kiểm tra venv ---
IF EXIST venv (
    call venv\Scripts\activate
    goto :end
)

:: --- Tải & cài Python nếu chưa có ---
set "PY_VERSION=3.12.7"
set "PY_URL=https://www.python.org/ftp/python/%PY_VERSION%/python-%PY_VERSION%-amd64.exe"
set "INSTALLER=python-installer.exe"

where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    powershell -Command "Invoke-WebRequest -Uri '%PY_URL%' -OutFile '%INSTALLER%'"
    start /wait "" "%INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del "%INSTALLER%"
)

:: --- Tạo và thiết lập môi trường ảo ---
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

:end

python download_music_youtube.py

endlocal
pause