# GPU Acceleration Guide

This guide explains how to set up GPU acceleration for the GGUF Loader App, which works exactly like LM Studio - automatically detecting and using your GPU when available, with seamless fallback to CPU.

## Overview

The GGUF Loader App provides **GPU acceleration** that:
- ✅ **Auto-detects** NVIDIA CUDA, Apple Metal, AMD ROCm, and Intel GPUs
- ✅ **Uses system drivers only** - no bundled GPU libraries
- ✅ **Falls back to CPU** automatically when GPU is unavailable
- ✅ **Works out of the box** if you have compatible drivers
- ✅ **Provides clear status** so you know what's being used

## Quick Setup

### Automatic Installation (Recommended)

Run the GPU setup script that automatically detects your hardware:

**Windows:**
```bash
setup_gpu.bat
```

**macOS/Linux:**
```bash
./setup_gpu.sh
```

The script will:
1. Detect your GPU hardware
2. Install the appropriate llama-cpp-python version
3. Test the installation
4. Provide clear feedback on success/failure

### Manual Installation

If you prefer manual control, install the appropriate version:

**NVIDIA GPU (CUDA):**
```bash
pip uninstall llama-cpp-python
pip install llama-cpp-python[cuda]
```

**AMD GPU (ROCm):**
```bash
pip uninstall llama-cpp-python
pip install llama-cpp-python[rocm]
```

**Intel GPU (Vulkan):**
```bash
pip uninstall llama-cpp-python
pip install llama-cpp-python[vulkan]
```

**Apple Silicon (Metal - macOS only):**
```bash
pip uninstall llama-cpp-python
pip install llama-cpp-python
```

## System Requirements

### NVIDIA CUDA
- **GPU**: NVIDIA GTX 1060 or newer (Compute Capability 6.1+)
- **Drivers**: NVIDIA Game Ready or Studio drivers
- **CUDA**: 11.8+ or 12.x (installed with drivers)
- **Memory**: 4GB+ VRAM recommended

### Apple Metal
- **System**: macOS 10.15+ (Catalina or newer)
- **Hardware**: Apple Silicon (M1/M2/M3) or Intel Mac with Metal support
- **Memory**: 8GB+ unified memory recommended

### AMD ROCm
- **GPU**: AMD RX 6000 series or newer, or Radeon Pro cards
- **System**: Linux (Ubuntu 20.04+, CentOS 8+)
- **Drivers**: AMDGPU-PRO or ROCm drivers
- **Memory**: 4GB+ VRAM recommended

### Intel GPU
- **GPU**: Intel Arc or Iris Xe graphics
- **System**: Windows 10+ or Linux
- **Drivers**: Latest Intel GPU drivers
- **Memory**: 4GB+ VRAM recommended

## Verification

### Test GPU Detection
Run the GPU test script to verify your setup:

```bash
python test_gpu_acceleration.py
```

Expected output with GPU:
```
=== GPU Detection Test ===
GPU Available: True
Backend: cuda
Status Message: NVIDIA GPU: GeForce RTX 4060 (8188 MB)
```

Expected output without GPU:
```
=== GPU Detection Test ===
GPU Available: False
Backend: cpu
Status Message: CPU only (no compatible GPU detected)
```

### Check in Application
1. Open the GGUF Loader App
2. Go to **Edit → Preferences → Model Settings**
3. Look at the **Hardware Acceleration** section
4. You should see your GPU status displayed

## Troubleshooting

### Common Issues

#### "No compatible GPU detected"
**Cause**: GPU drivers not installed or llama-cpp-python doesn't have GPU support

**Solutions**:
1. **Update GPU drivers**:
   - NVIDIA: Download from [nvidia.com/drivers](https://www.nvidia.com/drivers)
   - AMD: Download from [amd.com/support](https://www.amd.com/support)
   - Intel: Download from Intel support

2. **Reinstall GPU-enabled llama-cpp-python**:
   ```bash
   # Run the setup script again
   setup_gpu.bat  # Windows
   ./setup_gpu.sh # macOS/Linux
   ```

#### "CUDA out of memory" errors
**Cause**: Model too large for GPU memory

**Solutions**:
1. **Reduce GPU layers** in Preferences → Model Settings
2. **Use a smaller model**
3. **Close other GPU-using applications**

#### "Model loads slowly with GPU"
**Cause**: Incorrect GPU layer configuration

**Solutions**:
1. **Increase GPU layers** if you have VRAM available
2. **Check GPU utilization** with Task Manager (Windows) or Activity Monitor (macOS)

### Advanced Troubleshooting

#### Check llama-cpp-python GPU support
```python
import llama_cpp
print(f"CUDA support: {hasattr(llama_cpp, 'GGML_USE_CUBLAS')}")
print(f"Metal support: {hasattr(llama_cpp, 'GGML_USE_METAL')}")
```

#### Force CPU mode (for testing)
Set environment variable:
```bash
export GGML_FORCE_CPU=1  # Linux/macOS
set GGML_FORCE_CPU=1     # Windows
```

#### Check GPU memory usage
**NVIDIA**:
```bash
nvidia-smi
```

**AMD (Linux)**:
```bash
rocm-smi
```

**Apple**:
```bash
system_profiler SPDisplaysDataType
```

## Performance Tips

### Optimal GPU Layer Settings
- **4GB VRAM**: 10-20 layers
- **8GB VRAM**: 20-40 layers  
- **12GB VRAM**: 40-60 layers
- **16GB+ VRAM**: 60-100 layers (all layers)

### Memory Management
- **Close other GPU applications** (games, video editing, etc.)
- **Use smaller context sizes** for larger models
- **Monitor VRAM usage** to avoid out-of-memory errors

### Model Selection
- **Quantized models** (Q4, Q5, Q8) use less VRAM
- **Full precision models** (F16, F32) need more VRAM but may be more accurate

## How It Works

The GGUF Loader App uses a **smart detection system** similar to LM Studio:

1. **Hardware Detection**: Automatically detects your GPU using system commands
   - Windows/Linux: `nvidia-smi` for NVIDIA
   - macOS: `system_profiler` for Apple GPUs
   - Linux: `lspci` for AMD/Intel

2. **Software Validation**: Checks if llama-cpp-python has GPU support compiled in

3. **Automatic Configuration**: Calculates optimal settings based on your VRAM

4. **Seamless Fallback**: Falls back to CPU if GPU is unavailable or fails

5. **Clear Status**: Shows exactly what's being used in the UI and logs

## FAQ

**Q: Do I need to install CUDA separately?**
A: No, CUDA runtime is included with NVIDIA drivers. Just install the latest Game Ready or Studio drivers.

**Q: Will this work with my old GPU?**
A: NVIDIA GTX 1060+ and AMD RX 6000+ are supported. Older cards may work but aren't guaranteed.

**Q: Can I use both CPU and GPU?**
A: Yes, the app uses GPU for model layers and CPU for processing, automatically balancing the workload.

**Q: How much faster is GPU vs CPU?**
A: Typically 3-10x faster depending on your GPU and model size. Larger models see bigger improvements.

**Q: Does this increase power consumption?**
A: Yes, GPU acceleration uses more power but provides much faster inference. You can switch to CPU mode to save power.

## Support

If you encounter issues:

1. **Run the test script**: `python test_gpu_acceleration.py`
2. **Check the logs** in the application for detailed error messages
3. **Try the automatic setup script** again: `setup_gpu.bat` or `./setup_gpu.sh`
4. **Report issues** with your GPU model, drivers, and error messages

The system is designed to work like LM Studio - if it works there, it should work here too!