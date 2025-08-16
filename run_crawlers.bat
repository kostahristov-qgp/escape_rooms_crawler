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
