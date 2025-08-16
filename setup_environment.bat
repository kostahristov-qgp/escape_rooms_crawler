@echo off
setlocal

:: Change these if needed
set PYTHON_URL=https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe
set PYTHON_INSTALLER=python-installer.exe
set INSTALL_DIR=%USERPROFILE%\Python312
set REQUIREMENTS=requirements.txt

echo 🔍 Checking if Python is installed...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 🚀 Python not found. Downloading...
    powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %PYTHON_INSTALLER%"

    echo 🔧 Installing Python to %INSTALL_DIR%...
    %PYTHON_INSTALLER% /quiet InstallAllUsers=0 PrependPath=1 TargetDir=%INSTALL_DIR%

    if exist %PYTHON_INSTALLER% del %PYTHON_INSTALLER%

    set PATH=%INSTALL_DIR%;%INSTALL_DIR%\Scripts;%PATH%
    echo ✅ Python installed!
) else (
    echo ✅ Python is already installed!
)

echo 🔄 Refreshing environment...
refreshenv >nul 2>nul

:: Check pip
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ pip not found. Python installation may have failed.
    exit /b 1
)

:: Install packages
if exist %REQUIREMENTS% (
    echo 📦 Installing packages from %REQUIREMENTS%...
    pip install -r %REQUIREMENTS%
    echo ✅ Packages installed.
) else (
    echo ⚠️ requirements.txt not found.
)

pause