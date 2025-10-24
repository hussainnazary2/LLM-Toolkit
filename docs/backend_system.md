# Backend System Documentation

## Overview

The GGUF Loader App uses a flexible backend system that supports multiple inference engines for running GGUF models. This system provides automatic hardware detection, GPU acceleration, and graceful fallback mechanisms to ensure reliable model loading and inference across different hardware configurations.

## Architecture

The backend system consists of several key components:

- **Backend Abstraction Layer**: Common interface for all inference backends
- **Backend Manager**: Handles backend selection, switching, and fallback logic
- **Hardware Detector**: Identifies available GPUs and system capabilities
- **Configuration Manager**: Manages backend settings and user preferences

## Supported Backends

### 1. ctransformers Backend (Primary)

**Best for**: Most users, especially those with NVIDIA GPUs

**Advantages**:
- Easy installation with reliable prebuilt wheels
- Excellent GPU support (CUDA, ROCm, Metal)
- Good performance with GGUF models
- Minimal dependencies

**Installation**:
```bash
pip install ctransformers[cuda]  # For NVIDIA GPUs
pip install ctransformers[rocm]  # For AMD GPUs
pip install ctransformers        # CPU only
```

**Supported Hardware**:
- NVIDIA GPUs (CUDA 11.0+)
- AMD GPUs (ROCm 5.0+)
- Apple Silicon (Metal)
- CPU fallback

### 2. transformers + accelerate Backend

**Best for**: Users who need broad model support and latest features

**Advantages**:
- Excellent GPU acceleration
- Active development and updates
- Broad model format support
- Advanced optimization features

**Installation**:
```bash
pip install transformers accelerate torch
```

**Supported Hardware**:
- NVIDIA GPUs (CUDA)
- AMD GPUs (ROCm)
- Apple Silicon (MPS)
- CPU fallback

### 3. llamafile Backend

**Best for**: Users who want zero-dependency solutions

**Advantages**:
- Single executable, no Python dependencies
- Automatic GPU detection and optimization
- Cross-platform compatibility
- No installation issues

**Installation**:
- Download the appropriate llamafile executable
- No additional dependencies required

**Supported Hardware**:
- Automatic hardware detection
- NVIDIA, AMD, and Intel GPUs
- CPU fallback

### 4. llama-cpp-python Backend (Legacy)

**Best for**: Existing users with working installations

**Advantages**:
- Direct GGUF support
- Good performance when working
- Extensive customization options

**Disadvantages**:
- Complex installation requirements
- Frequent build failures
- CUDA toolkit dependencies

**Installation**:
```bash
pip install llama-cpp-python
```

## Backend Selection Logic

The system automatically selects the best available backend using this priority order:

1. **ctransformers** (if available and GPU compatible)
2. **transformers** (if available and GPU compatible)
3. **llamafile** (if executable found)
4. **llama-cpp-python** (fallback for existing installations)

### Manual Backend Selection

Users can override automatic selection through:
- Settings UI → Backend Selection
- Configuration file
- Environment variables

## Hardware Detection

The system automatically detects:

### GPU Information
- GPU vendor (NVIDIA, AMD, Intel)
- VRAM capacity
- Driver versions
- Compute capability

### System Information
- CPU cores and architecture
- System RAM
- Operating system
- Available disk space

### Optimization Recommendations
- Optimal backend for detected hardware
- Recommended GPU layer allocation
- Memory usage guidelines
- Performance tuning suggestions

## Configuration

### Backend Configuration File

Location: `~/.gguf-loader/backend_config.json`

```json
{
  "preferred_backend": "ctransformers",
  "gpu_enabled": true,
  "fallback_enabled": true,
  "backends": {
    "ctransformers": {
      "enabled": true,
      "priority": 1,
      "gpu_layers": -1,
      "context_size": 2048,
      "batch_size": 512
    },
    "transformers": {
      "enabled": true,
      "priority": 2,
      "device_map": "auto",
      "torch_dtype": "float16"
    }
  }
}
```

### Environment Variables

- `GGUF_BACKEND`: Force specific backend
- `GGUF_GPU_ENABLED`: Enable/disable GPU acceleration
- `GGUF_DEBUG`: Enable debug logging

## Performance Optimization

### GPU Layer Allocation

- **Small models (< 4GB)**: Use all GPU layers (-1)
- **Medium models (4-8GB)**: Use 75% of available VRAM
- **Large models (> 8GB)**: Use 50% of available VRAM

### Memory Management

- Monitor VRAM usage during inference
- Use model quantization for memory savings
- Enable memory mapping for large models
- Clear model cache between loads

### Batch Processing

- Increase batch size for better GPU utilization
- Use streaming for long text generation
- Enable parallel processing where supported

## Monitoring and Diagnostics

### Performance Metrics

The system tracks:
- Model loading times
- Inference speed (tokens/second)
- Memory usage (RAM and VRAM)
- GPU utilization percentage
- Error rates by backend

### Health Checks

Regular health checks verify:
- Backend availability
- GPU driver status
- Memory availability
- Model file integrity

### Diagnostic Tools

Built-in tools for:
- Backend compatibility testing
- Hardware benchmark testing
- Configuration validation
- Performance profiling

## Error Handling

### Automatic Recovery

The system automatically handles:
- Backend initialization failures
- GPU memory exhaustion
- Driver compatibility issues
- Model loading errors

### Fallback Mechanisms

1. **GPU to CPU fallback**: When GPU fails, switch to CPU mode
2. **Backend fallback**: When primary backend fails, try next available
3. **Graceful degradation**: Reduce model complexity if needed

### Error Reporting

Errors are categorized as:
- **Installation errors**: Missing dependencies or drivers
- **Hardware errors**: GPU or memory issues
- **Model errors**: File corruption or format issues
- **Configuration errors**: Invalid settings

## Migration Guide

### From llama-cpp-python

1. **Backup current configuration**:
   ```bash
   cp ~/.gguf-loader/config.json ~/.gguf-loader/config.json.backup
   ```

2. **Install preferred backend**:
   ```bash
   pip install ctransformers[cuda]
   ```

3. **Update configuration**:
   - Open Settings → Backend Selection
   - Choose "ctransformers" as preferred backend
   - Test with existing models

4. **Verify performance**:
   - Compare loading times
   - Check GPU utilization
   - Validate inference quality

### Configuration Migration

The system automatically migrates:
- Model paths and settings
- GPU configuration preferences
- Custom parameters
- User interface preferences

## Best Practices

### Installation
- Use virtual environments for Python backends
- Install GPU-specific packages for your hardware
- Verify installation with test models
- Keep drivers updated

### Configuration
- Start with default settings
- Adjust GPU layers based on VRAM
- Monitor memory usage during inference
- Use appropriate quantization levels

### Troubleshooting
- Check system requirements first
- Verify GPU driver compatibility
- Test with small models initially
- Enable debug logging for issues

### Performance
- Use GPU acceleration when available
- Optimize batch sizes for your hardware
- Monitor system resources
- Regular performance benchmarking

## Support and Resources

### Documentation
- [Troubleshooting Guide](troubleshooting_guide.md)
- [Performance Optimization](performance_optimization.md)
- [Hardware Compatibility](hardware_compatibility.md)
- [API Reference](api_reference.md)

### Community
- GitHub Issues for bug reports
- Discussions for questions and tips
- Wiki for community guides
- Discord for real-time support

### Updates
- Regular backend updates
- Hardware driver recommendations
- Performance improvements
- New feature announcements