@echo off
echo GGUF Loader App - GPU Support Installation
echo ==========================================
echo.
echo This script will install GPU-accelerated llama-cpp-python.
echo Make sure you have the appropriate GPU drivers installed:
echo   - NVIDIA: CUDA 11.8+ or 12.x drivers
echo   - AMD: ROCm 5.4+ drivers  
echo   - Intel: Latest GPU drivers
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Error: Virtual environment not found!
    echo Please run setup_env.bat first to create the virtual environment.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Detecting your GPU...
echo.

REM Detect NVIDIA GPU
nvidia-smi >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo NVIDIA GPU detected!
    echo.
    echo Installing CUDA-accelerated llama-cpp-python...
    echo This may take several minutes and download ~500MB...
    echo.
    
    REM Uninstall CPU version first
    pip uninstall -y llama-cpp-python
    
    REM Install CUDA version
    pip install llama-cpp-python[cuda] --upgrade --force-reinstall --no-cache-dir
    
    if %ERRORLEVEL% equ 0 (
        echo.
        echo ✅ CUDA support installed successfully!
        echo Your app will now use GPU acceleration automatically.
    ) else (
        echo.
        echo ❌ CUDA installation failed. Reinstalling CPU version...
        pip install llama-cpp-python>=0.2.0
        echo CPU version restored. GPU acceleration not available.
    )
    goto :end
)

REM Check for AMD GPU (basic detection)
wmic path win32_VideoController get name | findstr /i "AMD\|Radeon" >nul
if %ERRORLEVEL% equ 0 (
    echo AMD GPU detected!
    echo.
    echo Installing ROCm-accelerated llama-cpp-python...
    echo This may take several minutes and download ~500MB...
    echo.
    
    REM Uninstall CPU version first
    pip uninstall -y llama-cpp-python
    
    REM Install ROCm version
    pip install llama-cpp-python[rocm] --upgrade --force-reinstall --no-cache-dir
    
    if %ERRORLEVEL% equ 0 (
        echo.
        echo ✅ ROCm support installed successfully!
        echo Your app will now use GPU acceleration automatically.
    ) else (
        echo.
        echo ❌ ROCm installation failed. Reinstalling CPU version...
        pip install llama-cpp-python>=0.2.0
        echo CPU version restored. GPU acceleration not available.
    )
    goto :end
)

REM Check for Intel GPU
wmic path win32_VideoController get name | findstr /i "Intel" >nul
if %ERRORLEVEL% equ 0 (
    echo Intel GPU detected!
    echo.
    echo Installing Vulkan-accelerated llama-cpp-python...
    echo This may take several minutes and download ~300MB...
    echo.
    
    REM Uninstall CPU version first
    pip uninstall -y llama-cpp-python
    
    REM Install Vulkan version
    pip install llama-cpp-python[vulkan] --upgrade --force-reinstall --no-cache-dir
    
    if %ERRORLEVEL% equ 0 (
        echo.
        echo ✅ Vulkan support installed successfully!
        echo Your app will now use GPU acceleration automatically.
    ) else (
        echo.
        echo ❌ Vulkan installation failed. Reinstalling CPU version...
        pip install llama-cpp-python>=0.2.0
        echo CPU version restored. GPU acceleration not available.
    )
    goto :end
)

echo No compatible GPU detected or GPU drivers not installed.
echo.
echo If you have a GPU, make sure you have the latest drivers installed:
echo   - NVIDIA: Download from https://www.nvidia.com/drivers
echo   - AMD: Download from https://www.amd.com/support  
echo   - Intel: Download from https://www.intel.com/content/www/us/en/support/products/80939/graphics.html
echo.
echo The app will continue to work with CPU acceleration.

:end
echo.
echo Installation complete!
echo.
echo To test GPU acceleration, run:
echo     python test_gpu_acceleration.py
echo.
pause