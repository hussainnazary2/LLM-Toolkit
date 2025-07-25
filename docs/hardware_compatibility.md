# Hardware Compatibility Guide

## Overview

This guide provides comprehensive information about hardware compatibility for the GGUF Loader App's backend system. It covers GPU support, system requirements, and optimization recommendations for different hardware configurations.

## GPU Compatibility

### NVIDIA GPUs

#### Supported Architectures

| Architecture | Generation | Examples | CUDA Compute | Status |
|--------------|------------|----------|--------------|---------|
| Ada Lovelace | RTX 40 Series | RTX 4090, 4080, 4070 | 8.9 | ✅ Excellent |
| Ampere | RTX 30 Series | RTX 3090, 3080, 3070 | 8.6 | ✅ Excellent |
| Turing | RTX 20 Series | RTX 2080 Ti, 2070 | 7.5 | ✅ Very Good |
| Pascal | GTX 10 Series | GTX 1080 Ti, 1070 | 6.1 | ✅ Good |
| Maxwell | GTX 900 Series | GTX 980, 970 | 5.2 | ⚠️ Limited |
| Kepler | GTX 700 Series | GTX 780, 770 | 3.5 | ❌ Not Supported |

#### CUDA Requirements

**Minimum Requirements**:
- CUDA Compute Capability 5.0+
- CUDA Toolkit 11.0+
- Driver Version 450.80.02+

**Recommended**:
- CUDA Compute Capability 7.0+
- CUDA Toolkit 11.8+
- Driver Version 520.61.05+

#### Backend Compatibility

| Backend | NVIDIA Support | Min CUDA | Recommended |
|---------|----------------|----------|-------------|
| ctransformers | ✅ Excellent | 11.0 | 11.8+ |
| transformers | ✅ Excellent | 11.0 | 11.8+ |
| llamafile | ✅ Good | Auto-detect | Latest |
| llama-cpp-python | ✅ Good | 11.0 | 11.8+ |

#### Performance by GPU Class

**High-End (24GB+ VRAM)**:
- RTX 4090, A6000, RTX 3090
- Can run 70B+ models with Q4_0 quantization
- Excellent performance with all backends

**Mid-High (12-16GB VRAM)**:
- RTX 4070 Ti, RTX 3080 Ti, RTX 4080
- Can run 34B models with Q4_0, 13B with Q5_K_M
- Very good performance with all backends

**Mid-Range (8-12GB VRAM)**:
- RTX 3070, RTX 4060 Ti, RTX 2080 Ti
- Can run 13B models with Q4_0, 7B with Q5_K_M
- Good performance, may need optimization

**Entry-Level (4-8GB VRAM)**:
- GTX 1660, RTX 3050, GTX 1070
- Can run 7B models with Q4_0, 3B with Q5_K_M
- Adequate performance, CPU fallback recommended

### AMD GPUs

#### Supported Architectures

| Architecture | Generation | Examples | ROCm Support | Status |
|--------------|------------|----------|--------------|---------|
| RDNA 3 | RX 7000 Series | RX 7900 XTX, 7800 XT | 5.4+ | ✅ Excellent |
| RDNA 2 | RX 6000 Series | RX 6900 XT, 6700 XT | 5.0+ | ✅ Very Good |
| RDNA | RX 5000 Series | RX 5700 XT, 5600 XT | 4.5+ | ✅ Good |
| GCN 5.1 | Vega Series | Vega 64, Vega 56 | 4.0+ | ⚠️ Limited |
| GCN 4.0 | RX 400/500 | RX 580, RX 480 | 3.5+ | ⚠️ Limited |

#### ROCm Requirements

**Minimum Requirements**:
- ROCm 4.5+
- Linux (Ubuntu 20.04+, CentOS 8+)
- AMDGPU driver

**Recommended**:
- ROCm 5.4+
- Ubuntu 22.04 LTS
- Latest AMDGPU-PRO driver

#### Backend Compatibility

| Backend | AMD Support | Min ROCm | Notes |
|---------|-------------|----------|-------|
| transformers | ✅ Excellent | 5.0 | Best AMD support |
| ctransformers | ✅ Good | 5.0 | ROCm build required |
| llamafile | ✅ Good | Auto-detect | Automatic optimization |
| llama-cpp-python | ⚠️ Limited | 4.5 | Complex setup |

#### Windows Support

AMD GPU support on Windows is limited:
- No native ROCm support on Windows
- Use CPU backends or WSL2 with Linux
- Consider Intel Arc or NVIDIA for Windows

### Intel GPUs

#### Supported Architectures

| Architecture | Generation | Examples | Intel Support | Status |
|--------------|------------|----------|---------------|---------|
| Xe-HPG | Arc Series | Arc A770, A750 | Intel XPU | ✅ Good |
| Xe-LP | Iris Xe | Iris Xe Max | Intel XPU | ⚠️ Limited |
| UHD Graphics | Integrated | UHD 770, 630 | Intel XPU | ⚠️ Basic |

#### Intel XPU Requirements

**Requirements**:
- Intel GPU drivers 31.0.101.4146+
- Intel Extension for PyTorch
- Windows 11 or Linux

**Installation**:
```bash
# Install Intel Extension for PyTorch
pip install intel-extension-for-pytorch
pip install mkl
```

#### Backend Compatibility

| Backend | Intel Support | Requirements | Performance |
|---------|---------------|--------------|-------------|
| transformers | ✅ Good | Intel XPU | Good for Arc series |
| llamafile | ✅ Basic | Auto-detect | Basic acceleration |
| ctransformers | ❌ None | N/A | CPU fallback |
| llama-cpp-python | ⚠️ Experimental | Custom build | Variable |

### Apple Silicon (M1/M2/M3)

#### Supported Chips

| Chip | GPU Cores | Unified Memory | Status |
|------|-----------|----------------|---------|
| M3 Max | 40 | Up to 128GB | ✅ Excellent |
| M3 Pro | 18 | Up to 36GB | ✅ Excellent |
| M3 | 10 | Up to 24GB | ✅ Very Good |
| M2 Ultra | 76 | Up to 192GB | ✅ Excellent |
| M2 Max | 38 | Up to 96GB | ✅ Excellent |
| M2 Pro | 19 | Up to 32GB | ✅ Very Good |
| M2 | 10 | Up to 24GB | ✅ Very Good |
| M1 Ultra | 64 | Up to 128GB | ✅ Excellent |
| M1 Max | 32 | Up to 64GB | ✅ Very Good |
| M1 Pro | 16 | Up to 32GB | ✅ Good |
| M1 | 8 | Up to 16GB | ✅ Good |

#### Metal Performance Shaders

**Requirements**:
- macOS 12.0+ (Monterey)
- Metal Performance Shaders framework
- Unified memory architecture

**Backend Compatibility**:

| Backend | Apple Silicon | Metal Support | Performance |
|---------|---------------|---------------|-------------|
| ctransformers | ✅ Excellent | Yes | Very Good |
| transformers | ✅ Good | MPS backend | Good |
| llamafile | ✅ Good | Auto-detect | Good |
| llama-cpp-python | ✅ Good | Metal | Variable |

#### Memory Considerations

Apple Silicon uses unified memory:
- GPU and CPU share the same memory pool
- No separate VRAM limitation
- Can run larger models than discrete GPUs
- Memory bandwidth is excellent

## System Requirements

### Minimum Requirements

**CPU**:
- x86_64 architecture
- 4 cores, 2.0 GHz
- SSE4.1 support

**Memory**:
- 8GB RAM (16GB recommended)
- 10GB free disk space

**Operating System**:
- Windows 10 (1903+)
- Ubuntu 18.04+ / CentOS 8+
- macOS 11.0+ (Big Sur)

**Python**:
- Python 3.8-3.11
- pip 21.0+

### Recommended Requirements

**CPU**:
- Modern x86_64 or ARM64
- 8+ cores, 3.0+ GHz
- AVX2 support

**Memory**:
- 32GB+ RAM
- NVMe SSD storage
- 50GB+ free space

**GPU**:
- 8GB+ VRAM (discrete GPU)
- Latest drivers
- CUDA 11.8+ / ROCm 5.4+

## Performance Expectations

### Model Size Guidelines

#### 7B Parameter Models

**4GB VRAM**:
- Q4_0: Good performance
- Q5_K_M: Possible with optimization
- Q8_0: CPU fallback likely

**8GB VRAM**:
- Q4_0: Excellent performance
- Q5_K_M: Very good performance
- Q8_0: Good performance

**12GB+ VRAM**:
- All quantizations: Excellent performance
- Multiple models: Possible

#### 13B Parameter Models

**8GB VRAM**:
- Q4_0: Good performance
- Q5_K_M: Possible with optimization
- Q8_0: CPU fallback

**12GB VRAM**:
- Q4_0: Excellent performance
- Q5_K_M: Very good performance
- Q8_0: Good performance

**16GB+ VRAM**:
- All quantizations: Excellent performance

#### 34B Parameter Models

**16GB VRAM**:
- Q4_0: Good performance
- Q5_K_M: Limited
- Q8_0: CPU fallback

**24GB VRAM**:
- Q4_0: Excellent performance
- Q5_K_M: Very good performance
- Q8_0: Good performance

#### 70B Parameter Models

**24GB VRAM**:
- Q4_0: Good performance
- Q5_K_M: Limited
- Q8_0: CPU fallback

**48GB+ VRAM**:
- Q4_0: Excellent performance
- Q5_K_M: Very good performance
- Q8_0: Good performance

### Performance Benchmarks

#### Tokens per Second (Typical)

**NVIDIA RTX 4090 (24GB)**:
- 7B Q4_0: 80-120 tok/s
- 13B Q4_0: 45-65 tok/s
- 34B Q4_0: 18-25 tok/s
- 70B Q4_0: 8-12 tok/s

**NVIDIA RTX 3080 (10GB)**:
- 7B Q4_0: 60-90 tok/s
- 13B Q4_0: 30-45 tok/s
- 34B Q4_0: CPU fallback

**AMD RX 7900 XTX (24GB)**:
- 7B Q4_0: 50-80 tok/s
- 13B Q4_0: 25-40 tok/s
- 34B Q4_0: 12-18 tok/s

**Apple M2 Max (96GB)**:
- 7B Q4_0: 40-60 tok/s
- 13B Q4_0: 20-35 tok/s
- 34B Q4_0: 8-15 tok/s
- 70B Q4_0: 4-8 tok/s

## Hardware-Specific Optimizations

### NVIDIA Optimizations

**Driver Settings**:
```bash
# Enable persistence mode
sudo nvidia-smi -pm 1

# Set maximum performance
sudo nvidia-smi -ac 877,1215  # Memory,Graphics clocks

# Disable ECC (if not needed)
sudo nvidia-smi --ecc-config=0
```

**CUDA Optimizations**:
```json
{
  "cuda_optimizations": {
    "use_fast_math": true,
    "enable_tensor_cores": true,
    "memory_pool_size": 2048,
    "cuda_graphs": true
  }
}
```

### AMD Optimizations

**ROCm Settings**:
```bash
# Set performance mode
echo performance | sudo tee /sys/class/drm/card0/device/power_dpm_force_performance_level

# Increase power limit
echo 300 | sudo tee /sys/class/drm/card0/device/hwmon/hwmon0/power1_cap
```

**Configuration**:
```json
{
  "rocm_optimizations": {
    "hip_visible_devices": "0",
    "rocm_version": "5.4",
    "use_flash_attention": true
  }
}
```

### Apple Silicon Optimizations

**Metal Settings**:
```json
{
  "metal_optimizations": {
    "metal_performance_shaders": true,
    "unified_memory_optimization": true,
    "neural_engine": true
  }
}
```

**System Settings**:
```bash
# Disable App Nap
defaults write com.yourapp.ggufloader NSAppSleepDisabled -bool YES

# Optimize memory pressure
sudo sysctl -w vm.pressure_disable_threshold=15
```

## Troubleshooting Hardware Issues

### GPU Not Detected

**NVIDIA**:
```bash
# Check driver installation
nvidia-smi

# Verify CUDA
nvcc --version
python -c "import torch; print(torch.cuda.is_available())"

# Check compute capability
python -c "import torch; print(torch.cuda.get_device_capability())"
```

**AMD**:
```bash
# Check ROCm installation
rocm-smi

# Verify PyTorch ROCm
python -c "import torch; print(torch.cuda.is_available())"

# Check device
python -c "import torch; print(torch.cuda.get_device_name())"
```

**Intel**:
```bash
# Check Intel GPU
intel_gpu_top

# Verify Intel Extension
python -c "import intel_extension_for_pytorch as ipex; print(ipex.xpu.is_available())"
```

### Performance Issues

**Thermal Throttling**:
- Monitor GPU temperatures
- Improve case ventilation
- Adjust fan curves
- Consider undervolting

**Power Limitations**:
- Check PSU capacity
- Monitor power draw
- Adjust power limits
- Use separate PCIe cables

**Memory Bandwidth**:
- Check memory speeds
- Enable XMP/DOCP profiles
- Monitor memory usage
- Consider memory upgrades

### Driver Issues

**NVIDIA**:
```bash
# Clean driver installation
sudo apt purge nvidia-*
sudo apt autoremove
sudo apt install nvidia-driver-525

# Or use NVIDIA installer
sudo ./NVIDIA-Linux-x86_64-525.60.11.run --uninstall
sudo ./NVIDIA-Linux-x86_64-525.60.11.run
```

**AMD**:
```bash
# Install AMDGPU driver
sudo apt install amdgpu-dkms rocm-dev

# Or use AMD installer
sudo ./amdgpu-install --usecase=rocm
```

## Hardware Recommendations

### Budget Build (Under $500)

**GPU**: NVIDIA GTX 1660 Super (6GB) or AMD RX 5600 XT (6GB)
**CPU**: AMD Ryzen 5 3600 or Intel i5-10400
**RAM**: 16GB DDR4-3200
**Storage**: 500GB NVMe SSD

**Capabilities**:
- 7B models with Q4_0 quantization
- Good performance for chat applications
- CPU fallback for larger models

### Mid-Range Build ($500-$1500)

**GPU**: NVIDIA RTX 3070 (8GB) or AMD RX 6700 XT (12GB)
**CPU**: AMD Ryzen 7 5700X or Intel i7-12700
**RAM**: 32GB DDR4-3600
**Storage**: 1TB NVMe SSD

**Capabilities**:
- 13B models with Q4_0/Q5_K_M quantization
- Excellent performance for most use cases
- Some 34B model support

### High-End Build ($1500-$3000)

**GPU**: NVIDIA RTX 4080 (16GB) or RTX 3080 Ti (12GB)
**CPU**: AMD Ryzen 9 5900X or Intel i9-12900K
**RAM**: 64GB DDR4-3600 or DDR5-5600
**Storage**: 2TB NVMe SSD

**Capabilities**:
- 34B models with Q4_0 quantization
- 13B models with Q8_0 quantization
- Excellent performance across all backends

### Enthusiast Build ($3000+)

**GPU**: NVIDIA RTX 4090 (24GB) or dual RTX 4080
**CPU**: AMD Ryzen 9 7950X or Intel i9-13900K
**RAM**: 128GB DDR5-5600
**Storage**: 4TB NVMe SSD

**Capabilities**:
- 70B models with Q4_0 quantization
- 34B models with Q8_0 quantization
- Multiple model loading
- Research and development workloads

## Future Hardware Support

### Upcoming Technologies

**NVIDIA**:
- RTX 50 Series (Blackwell architecture)
- Improved tensor cores
- Higher memory bandwidth

**AMD**:
- RDNA 4 architecture
- Better AI acceleration
- Improved ROCm support

**Intel**:
- Arc Battlemage GPUs
- Enhanced XPU support
- Better Windows compatibility

### Emerging Standards

**Memory**:
- HBM3 for high-end GPUs
- DDR5 becoming standard
- Larger VRAM capacities

**Interconnects**:
- PCIe 5.0 adoption
- NVLink improvements
- Infinity Cache enhancements

**Software**:
- Better cross-platform support
- Improved quantization methods
- Enhanced memory management

## Compatibility Matrix

### Quick Reference

| Hardware | ctransformers | transformers | llamafile | llama-cpp-python |
|----------|---------------|--------------|-----------|------------------|
| NVIDIA RTX 40 | ✅ Excellent | ✅ Excellent | ✅ Good | ✅ Good |
| NVIDIA RTX 30 | ✅ Excellent | ✅ Excellent | ✅ Good | ✅ Good |
| NVIDIA GTX 16 | ✅ Good | ✅ Good | ✅ Good | ✅ Good |
| AMD RX 7000 | ✅ Good | ✅ Excellent | ✅ Good | ⚠️ Limited |
| AMD RX 6000 | ✅ Good | ✅ Very Good | ✅ Good | ⚠️ Limited |
| Intel Arc | ❌ None | ✅ Good | ✅ Basic | ❌ None |
| Apple M1/M2/M3 | ✅ Excellent | ✅ Good | ✅ Good | ✅ Good |
| CPU Only | ✅ Good | ✅ Good | ✅ Excellent | ✅ Good |

### Legend
- ✅ Excellent: Full support, optimal performance
- ✅ Very Good: Full support, good performance
- ✅ Good: Supported, adequate performance
- ⚠️ Limited: Partial support, may have issues
- ❌ None: Not supported

This compatibility guide should help you choose the right hardware and backend combination for your specific needs and budget.