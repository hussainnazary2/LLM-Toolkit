@echo off
echo Setting up virtual environment for GGUF Loader App...

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8 or higher.
    exit /b 1
)

REM Check Python version
python -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"
if %ERRORLEVEL% neq 0 (
    echo Python 3.8 or higher is required. Please update your Python installation.
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment and install dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Virtual environment setup complete!
echo.
echo To activate the virtual environment, run:
echo     venv\Scripts\activate.bat
echo.
echo To deactivate the virtual environment, run:
echo     deactivate
echo.