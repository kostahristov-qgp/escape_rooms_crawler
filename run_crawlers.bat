@echo off
setlocal
set PYTHONIOENCODING=utf-8

REM
set TF_CPP_MIN_LOG_LEVEL=3
set ABSL_LOG_STDERR_THRESHOLD=FATAL

REM Create logs folder if it doesn't exist
if not exist logs mkdir logs

REM Get current date and time in safe format for filenames
for /f %%A in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH-mm"') do set DATETIME=%%A
set LOGFILE=logs\%DATETIME%.log

REM Check if websites_list.txt exists
if not exist websites_list.txt (
    echo websites_list.txt not found! >> %LOGFILE%
    echo websites_list.txt not found!
    pause
    exit /b 1
)

REM Main loop - calls :RunScript with each script name
for /f "usebackq tokens=*" %%N in ("websites_list.txt") do (
    call :RunScript "%%N.py"
)

echo All crawlers finished. Log saved to %LOGFILE%
pause
exit /b

:RunScript
set "SCRIPT=%~1"

if exist "%SCRIPT%" (
    for /f %%T in ('powershell -NoProfile -Command "Get-Date -Format ''yyyy-MM-dd HH:mm:ss''"') do set NOW=%%T
    echo [%NOW%] Running %SCRIPT%... >> %LOGFILE%
    echo Running %SCRIPT%...
    python "%SCRIPT%" >> %LOGFILE% 2>&1

    for /f %%T in ('powershell -NoProfile -Command "Get-Date -Format ''yyyy-MM-dd HH:mm:ss''"') do set NOW=%%T
    echo [%NOW%] Finished %SCRIPT% >> %LOGFILE%
    echo Finished %SCRIPT%
    echo Sleeping 20 seconds...
    timeout /t 20 >nul
)

goto :eof