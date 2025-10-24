# Troubleshooting Guide

This guide covers general troubleshooting for llm toolkit. For format-specific issues, see the [Format-Specific Troubleshooting Guide](format_troubleshooting.md).

## Common Issues and Solutions

### GPU Detection Issues

#### Problem: GPU not detected or recognized

**Symptoms**:
- App shows "CPU only" mode
- No GPU options in settings
- Hardware detection shows no GPUs

**Solutions**:

1. **Check GPU drivers**:
   ```bash
   # For NVIDIA
   nvidia-smi
   
   # For AMD
   rocm-smi
   
   # For Intel
   intel_gpu_top
   ```

2. **Update drivers**:
   - NVIDIA: Download from [NVIDIA Driver Downloads](https://www.nvidia.com/drivers/)
   - AMD: Download from [AMD Driver Downloads](https://www.amd.com/support)
   - Intel: Update through Windows Update or Intel Driver Assistant

3. **Verify CUDA installation** (NVIDIA):
   ```bash
   nvcc --version
   python -c "import torch; print(torch.cuda.is_available())"
   ```

4. **Check ROCm installation** (AMD):
   ```bash
   rocm-smi --version
   python -c "import torch; print(torch.cuda.is_available())"
   ```

#### Problem: GPU detected but not used

**Symptoms**:
- GPU appears in system but app uses CPU
- Low GPU utilization during inference
- Slower than expected performance

**Solutions**:

1. **Check backend GPU support**:
   - Ensure selected backend supports your GPU
   - Try switching to ctransformers backend
   - Verify GPU layers setting > 0

2. **Memory allocation**:
   - Check available VRAM: `nvidia-smi` or `rocm-smi`
   - Reduce GPU layers if VRAM insufficient
   - Close other GPU-using applications

3. **Backend configuration**:
   ```json
   {
     "backends": {
       "ctransformers": {
         "gpu_layers": -1,
         "gpu_enabled": true
       }
     }
   }
   ```

### Installation Issues

#### Problem: Backend installation fails

**Symptoms**:
- pip install errors
- Missing dependencies
- Compilation failures

**Solutions**:

1. **Use prebuilt wheels**:
   ```bash
   # Instead of building from source
   pip install ctransformers[cuda] --no-build-isolation
   ```

2. **Check Python version compatibility**:
   - Use Python 3.8-3.11 (most compatible)
   - Avoid Python 3.12+ for some backends

3. **Virtual environment**:
   ```bash
   python -m venv gguf_env
   gguf_env\Scripts\activate  # Windows
   source gguf_env/bin/activate  # Linux/Mac
   pip install --upgrade pip
   ```

4. **Clear pip cache**:
   ```bash
   pip cache purge
   pip install --no-cache-dir ctransformers[cuda]
   ```

#### Problem: CUDA toolkit conflicts

**Symptoms**:
- Multiple CUDA versions detected
- Runtime version mismatches
- Library loading errors

**Solutions**:

1. **Check CUDA versions**:
   ```bash
   nvcc --version
   nvidia-smi  # Check driver version
   ```

2. **Use conda for CUDA management**:
   ```bash
   conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
   ```

3. **Set CUDA environment variables**:
   ```bash
   set CUDA_HOME=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8
   set PATH=%CUDA_HOME%\bin;%PATH%
   ```

### Model Loading Issues

#### Problem: Model fails to load

**Symptoms**:
- "Failed to load model" error
- Out of memory errors
- Corrupted model warnings
- Format detection failures

**Solutions**:

1. **Check model file integrity**:
   - Verify file size matches expected
   - Re-download if corrupted
   - Check file permissions
   - Ensure file is in a supported format (GGUF, safetensors, PyTorch, HF)

2. **Format-specific troubleshooting**:
   - See [Format-Specific Troubleshooting Guide](format_troubleshooting.md)
   - Check format detection results
   - Try manual format specification

2. **Memory management**:
   - Reduce GPU layers for large models
   - Close other applications
   - Use model quantization

3. **Backend compatibility**:
   - Try different backend (ctransformers → transformers)
   - Check model format support
   - Use llamafile for problematic models

4. **Performance optimization troubleshooting**:
   - Check if automatic backend selection is working: Look for "Optimization recommendation" in logs
   - Verify GPU layer optimization: Check for "Optimized GPU layers" messages
   - Monitor performance caching: Look for "Loaded performance cache" messages
   - Test with performance target settings: Try 'speed', 'balanced', or 'quality' modes

#### Problem: Performance optimization not working

**Symptoms**:
- No optimization messages in logs
- Backend selection seems random
- GPU layers not optimized
- Poor performance despite good hardware

**Solutions**:

1. **Enable performance optimization**:
   ```python
   from app.core.performance_integration import PerformanceIntegratedBackendManager
   manager = PerformanceIntegratedBackendManager()
   result = manager.load_model_optimized(
       model_path="your_model.gguf",
       hardware_preference="auto",
       performance_target="balanced"
   )
   ```

2. **Check optimization logs**:
   - Look for "Performance optimizer started" message
   - Verify "Hardware analysis" information is correct
   - Check for "Optimization recommendation" with confidence scores

3. **Verify hardware detection**:
   ```python
   from app.core.hardware_detector import HardwareDetector
   detector = HardwareDetector()
   info = detector.get_hardware_info()
   print(f"GPUs: {info.gpu_count}, VRAM: {info.total_vram}MB")
   ```

4. **Clear performance cache if needed**:
   ```python
   from app.core.performance_optimizer import PerformanceOptimizer
   optimizer = PerformanceOptimizer(detector)
   optimizer.clear_performance_cache()  # Clear all cache
   # or
   optimizer.clear_performance_cache("specific_model.gguf")  # Clear specific model
   ```

#### Problem: Out of memory errors

**Symptoms**:
- CUDA out of memory
- System RAM exhausted
- App crashes during loading

**Solutions**:

1. **Reduce GPU layers**:
   ```json
   {
     "gpu_layers": 20  // Instead of -1 (all layers)
   }
   ```

2. **Use smaller context size**:
   ```json
   {
     "context_size": 1024  // Instead of 4096
   }
   ```

3. **Enable memory mapping**:
   ```json
   {
     "use_mmap": true,
     "use_mlock": false
   }
   ```

4. **Model quantization**:
   - Use Q4_0 instead of Q8_0
   - Try Q2_K for very limited memory
   - Consider smaller model variants

### Performance Issues

#### Problem: Slow inference speed

**Symptoms**:
- Low tokens per second
- High latency
- Poor GPU utilization

**Solutions**:

1. **Optimize GPU layers**:
   - Start with all layers on GPU (-1)
   - Reduce if memory issues occur
   - Monitor VRAM usage

2. **Batch size optimization**:
   ```json
   {
     "batch_size": 512,  // Increase for better GPU utilization
     "n_threads": 8      // Optimize for CPU cores
   }
   ```

3. **Backend selection**:
   - Try ctransformers for GGUF models
   - Use transformers for broader support
   - Test llamafile for comparison

4. **System optimization**:
   - Close unnecessary applications
   - Ensure adequate cooling
   - Check power management settings

#### Problem: High memory usage

**Symptoms**:
- System becomes unresponsive
- Swap file usage increases
- Memory warnings

**Solutions**:

1. **Model size optimization**:
   - Use appropriate quantization level
   - Choose smaller model variants
   - Enable memory mapping

2. **Context management**:
   - Reduce context window size
   - Clear conversation history regularly
   - Use streaming for long outputs

3. **System configuration**:
   - Increase virtual memory
   - Close browser tabs and applications
   - Monitor memory usage

### Backend-Specific Issues

#### ctransformers Issues

**Common problems**:
- Installation on older systems
- GPU detection failures
- Model format compatibility

**Solutions**:
```bash
# Reinstall with specific GPU support
pip uninstall ctransformers
pip install ctransformers[cuda]  # or [rocm] for AMD

# Check installation
python -c "from ctransformers import AutoModelForCausalLM; print('OK')"
```

#### transformers Issues

**Common problems**:
- Large dependency size
- Model conversion needed
- Memory usage

**Solutions**:
```bash
# Install with specific torch version
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Check GPU support
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

#### llamafile Issues

**Common problems**:
- Executable permissions
- Antivirus blocking
- Process management

**Solutions**:
```bash
# Set executable permissions (Linux/Mac)
chmod +x llamafile

# Windows: Add to antivirus exceptions
# Check process status in Task Manager
```

### Network and Download Issues

#### Problem: Model download failures

**Symptoms**:
- Connection timeouts
- Partial downloads
- Corrupted files

**Solutions**:

1. **Use download managers**:
   - wget with resume capability
   - aria2c for parallel downloads
   - Browser download managers

2. **Mirror sites**:
   - Try different model repositories
   - Use local mirrors if available
   - Check repository status

3. **Network configuration**:
   - Disable VPN temporarily
   - Check firewall settings
   - Use wired connection for large files

### System-Specific Issues

#### Windows Issues

**Common problems**:
- Path length limitations
- Permission errors
- Antivirus interference

**Solutions**:
- Enable long path support in Windows
- Run as administrator if needed
- Add exceptions to antivirus
- Use shorter installation paths

#### Linux Issues

**Common problems**:
- Missing system libraries
- Permission issues
- Driver conflicts

**Solutions**:
```bash
# Install system dependencies
sudo apt update
sudo apt install build-essential python3-dev

# Fix permissions
sudo usermod -a -G video $USER
```

#### macOS Issues

**Common problems**:
- Apple Silicon compatibility
- Xcode command line tools
- Metal performance shaders

**Solutions**:
```bash
# Install Xcode tools
xcode-select --install

# Use Metal backend for Apple Silicon
pip install ctransformers  # Includes Metal support
```

## Diagnostic Tools

### Built-in Diagnostics

1. **Hardware Check**:
   - Settings → Diagnostics → Hardware Test
   - Verifies GPU detection and capabilities

2. **Backend Test**:
   - Settings → Diagnostics → Backend Test
   - Tests all available backends

3. **Performance Benchmark**:
   - Settings → Diagnostics → Benchmark
   - Measures loading and inference speed

### Manual Diagnostics

1. **System Information**:
   ```python
   from app.core.hardware_detector import HardwareDetector
   detector = HardwareDetector()
   print(detector.get_hardware_info().to_dict())
   ```

2. **Backend Status**:
   ```python
   from app.core.backend_manager import BackendManager
   manager = BackendManager()
   print(manager.get_statistics())
   ```

3. **Model Information**:
   ```python
   from app.models.gguf_model import GGUFModel
   model = GGUFModel("path/to/model.gguf")
   print(model.get_model_info())
   ```

4. **Performance Optimization Diagnostics**:
   ```python
   from app.core.performance_integration import PerformanceIntegratedBackendManager
   
   # Initialize optimized manager
   manager = PerformanceIntegratedBackendManager()
   
   # Get comprehensive performance insights
   insights = manager.get_performance_insights()
   print("Performance Insights:", insights)
   
   # Get optimization recommendations
   recommendations = manager.get_optimization_recommendations()
   print("Recommendations:", recommendations)
   
   # Run benchmark if model is loaded
   if manager.current_backend:
       benchmark = manager.run_comprehensive_benchmark(num_iterations=3)
       print("Benchmark Results:", benchmark)
   ```

5. **Performance Cache Diagnostics**:
   ```python
   from app.core.performance_optimizer import PerformanceOptimizer
   from app.core.hardware_detector import HardwareDetector
   
   detector = HardwareDetector()
   optimizer = PerformanceOptimizer(detector)
   
   # Get performance statistics
   stats = optimizer.get_performance_stats()
   print("Cache Stats:", stats)
   
   # Get optimization insights
   insights = optimizer.get_optimization_insights()
   print("Optimization Insights:", insights)
   
   # Export performance report
   optimizer.export_performance_report("performance_report.json")
   ```

6. **Batch Processing Diagnostics**:
   ```python
   # Check batch processor status
   batch_stats = optimizer.batch_processor.get_queue_stats()
   print("Batch Processing Stats:", batch_stats)
   ```

## Getting Help

### Before Reporting Issues

1. **Check system requirements**
2. **Update drivers and software**
3. **Try different backends**
4. **Review error logs**
5. **Test with small models**

### Information to Include

When reporting issues, include:
- Operating system and version
- GPU model and driver version
- Python version and backend versions
- Model file details
- Complete error messages
- Steps to reproduce

### Support Channels

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Questions and community help
- **Wiki**: Community guides and tips
- **Discord**: Real-time support and chat

### Log Files

Important log locations:
- Application logs: `~/.gguf-loader/logs/`
- Backend logs: `~/.gguf-loader/backend_logs/`
- System logs: Check Event Viewer (Windows) or syslog (Linux)

## Prevention Tips

### Regular Maintenance

1. **Keep drivers updated**
2. **Monitor disk space**
3. **Clear temporary files**
4. **Update backends regularly**
5. **Backup configurations**

### Best Practices

1. **Use virtual environments**
2. **Test with small models first**
3. **Monitor system resources**
4. **Keep multiple backends available**
5. **Document working configurations**

### Performance Monitoring

1. **Track loading times**
2. **Monitor memory usage**
3. **Check GPU utilization**
4. **Benchmark regularly**
5. **Profile bottlenecks**