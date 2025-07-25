@echo off
REM Launcher script for GGUF Loader App on Windows

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Creating one...
    call setup_env.bat
)

REM Activate virtual environment and run the application
echo Starting GGUF Loader App...
call venv\Scripts\activate.bat
python main.py %*

REM If there was an error, pause to show the message
if %ERRORLEVEL% neq 0 (
    echo.
    echo Application exited with error code %ERRORLEVEL%
    pause
)