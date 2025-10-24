#!/bin/bash

echo "GGUF Loader App - GPU Support Installation"
echo "=========================================="
echo ""
echo "This script will install GPU-accelerated llama-cpp-python."
echo "Make sure you have the appropriate GPU drivers installed:"
echo "  - NVIDIA: CUDA 11.8+ or 12.x drivers"
echo "  - AMD: ROCm 5.4+ drivers"
echo "  - Apple: macOS 10.15+ (Metal built-in)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run setup_env.sh first to create the virtual environment."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo "Detecting your system and GPU..."
echo ""

# Detect macOS (Metal support built-in)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS detected - Metal GPU support available!"
    echo ""
    echo "Installing Metal-accelerated llama-cpp-python..."
    echo "This may take several minutes and download ~300MB..."
    echo ""
    
    # Uninstall CPU version first
    pip uninstall -y llama-cpp-python
    
    # Install with Metal support (should be default on macOS)
    pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Metal support installed successfully!"
        echo "Your app will now use GPU acceleration automatically on Apple Silicon."
    else
        echo ""
        echo "❌ Installation failed. Reinstalling CPU version..."
        pip install "llama-cpp-python>=0.2.0"
        echo "CPU version restored. GPU acceleration not available."
    fi
    exit 0
fi

# Detect NVIDIA GPU on Linux
if command -v nvidia-smi &> /dev/null; then
    if nvidia-smi &> /dev/null; then
        echo "NVIDIA GPU detected!"
        echo ""
        echo "Installing CUDA-accelerated llama-cpp-python..."
        echo "This may take several minutes and download ~500MB..."
        echo ""
        
        # Uninstall CPU version first
        pip uninstall -y llama-cpp-python
        
        # Install CUDA version
        pip install 'llama-cpp-python[cuda]' --upgrade --force-reinstall --no-cache-dir
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ CUDA support installed successfully!"
            echo "Your app will now use GPU acceleration automatically."
        else
            echo ""
            echo "❌ CUDA installation failed. Reinstalling CPU version..."
            pip install "llama-cpp-python>=0.2.0"
            echo "CPU version restored. GPU acceleration not available."
        fi
        exit 0
    fi
fi

# Check for AMD GPU on Linux
if lspci | grep -i "amd\|radeon" &> /dev/null; then
    echo "AMD GPU detected!"
    echo ""
    echo "Installing ROCm-accelerated llama-cpp-python..."
    echo "This may take several minutes and download ~500MB..."
    echo ""
    
    # Uninstall CPU version first
    pip uninstall -y llama-cpp-python
    
    # Install ROCm version
    pip install 'llama-cpp-python[rocm]' --upgrade --force-reinstall --no-cache-dir
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ ROCm support installed successfully!"
        echo "Your app will now use GPU acceleration automatically."
    else
        echo ""
        echo "❌ ROCm installation failed. Reinstalling CPU version..."
        pip install "llama-cpp-python>=0.2.0"
        echo "CPU version restored. GPU acceleration not available."
    fi
    exit 0
fi

# Check for Intel GPU on Linux
if lspci | grep -i "intel.*graphics\|intel.*display" &> /dev/null; then
    echo "Intel GPU detected!"
    echo ""
    echo "Installing Vulkan-accelerated llama-cpp-python..."
    echo "This may take several minutes and download ~300MB..."
    echo ""
    
    # Uninstall CPU version first
    pip uninstall -y llama-cpp-python
    
    # Install Vulkan version
    pip install 'llama-cpp-python[vulkan]' --upgrade --force-reinstall --no-cache-dir
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Vulkan support installed successfully!"
        echo "Your app will now use GPU acceleration automatically."
    else
        echo ""
        echo "❌ Vulkan installation failed. Reinstalling CPU version..."
        pip install "llama-cpp-python>=0.2.0"
        echo "CPU version restored. GPU acceleration not available."
    fi
    exit 0
fi

echo "No compatible GPU detected or GPU drivers not installed."
echo ""
echo "If you have a GPU, make sure you have the latest drivers installed:"
echo "  - NVIDIA: Install CUDA toolkit and drivers"
echo "  - AMD: Install ROCm drivers"
echo "  - Intel: Install latest GPU drivers"
echo ""
echo "The app will continue to work with CPU acceleration."
echo ""
echo "Installation complete!"
echo ""
echo "To test GPU acceleration, run:"
echo "    python test_gpu_acceleration.py"