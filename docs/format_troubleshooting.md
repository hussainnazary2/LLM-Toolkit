# Format-Specific Troubleshooting Guide

This guide provides troubleshooting solutions for each supported model format in llm toolkit.

## Table of Contents

1. [GGUF Format Issues](#gguf-format-issues)
2. [Safetensors Format Issues](#safetensors-format-issues)
3. [PyTorch Bin Format Issues](#pytorch-bin-format-issues)
4. [Hugging Face Model Issues](#hugging-face-model-issues)
5. [Cross-Format Issues](#cross-format-issues)
6. [Backend Selection Issues](#backend-selection-issues)

## GGUF Format Issues

### Problem: GGUF file fails to load

**Symptoms**:
- "Invalid GGUF header" error
- "Unsupported GGUF version" warning
- File appears corrupted

**Solutions**:

1. **Check GGUF version compatibility**:
   ```python
   from app.core.universal_format_detector import UniversalFormatDetector
   detector = UniversalFormatDetector()
   result = detector.detect_format("your_model.gguf")
   print(f"Format: {result.format_type}, Version: {result.version}")
   ```

2. **Verify file integrity**:
   - Re-download the model file
   - Check file size matches expected size
   - Verify checksum if available
   - Ensure download completed successfully

3. **Try different backends**:
   - llama-cpp-python (primary for GGUF)
   - llamafile (alternative)
   - Check backend compatibility with GGUF version

4. **Version tolerance mode**:
   - Enable version-tolerant loading in settings
   - Use compatibility mode for older GGUF versions
   - Check for model conversion tools if needed

### Problem: GGUF metadata extraction fails

**Symptoms**:
- Missing model information
- "Failed to parse metadata" error
- Incomplete model details

**Solutions**:

1. **Enable graceful degradation**:
   ```python
   from app.core.universal_metadata_extractor import UniversalMetadataExtractor
   extractor = UniversalMetadataExtractor()
   metadata = extractor.extract_metadata("model.gguf", "gguf", graceful=True)
   ```

2. **Manual parameter estimation**:
   - Use file size for parameter estimation
   - Check model filename for hints
   - Use default settings for unknown architectures

3. **Update GGUF parser**:
   - Ensure latest version of llm toolkit
   - Check for GGUF specification updates
   - Report parsing issues for new GGUF versions

### Problem: GGUF model performance issues

**Symptoms**:
- Slow loading times
- High memory usage
- Poor inference speed

**Solutions**:

1. **Optimize GPU layers**:
   ```json
   {
     "backends": {
       "llama_cpp_python": {
         "gpu_layers": -1,
         "use_mmap": true,
         "use_mlock": false
       }
     }
   }
   ```

2. **Quantization optimization**:
   - Use appropriate quantization level (Q4_0, Q8_0)
   - Balance quality vs. performance
   - Consider model size vs. available memory

3. **Backend tuning**:
   - Adjust context size
   - Optimize batch size
   - Configure thread count

## Safetensors Format Issues

### Problem: Safetensors file fails to load

**Symptoms**:
- "Invalid safetensors header" error
- "Tensor loading failed" message
- Corrupted tensor data warnings

**Solutions**:

1. **Verify safetensors installation**:
   ```bash
   pip install safetensors
   python -c "import safetensors; print('OK')"
   ```

2. **Check file integrity**:
   ```python
   from safetensors import safe_open
   try:
       with safe_open("model.safetensors", framework="pt") as f:
           print("File is valid")
           print(f"Keys: {f.keys()}")
   except Exception as e:
       print(f"File error: {e}")
   ```

3. **Use transformers backend**:
   - Safetensors files require transformers backend
   - Ensure transformers is properly installed
   - Check for PyTorch compatibility

4. **Memory considerations**:
   - Safetensors files can be large
   - Ensure sufficient RAM/VRAM
   - Use memory mapping when possible

### Problem: Safetensors metadata missing

**Symptoms**:
- No model configuration found
- Missing tokenizer information
- Unknown model architecture

**Solutions**:

1. **Check for config.json**:
   - Look for config.json in same directory
   - Download from Hugging Face if missing
   - Use model card information

2. **Manual configuration**:
   ```python
   # Provide manual config for unknown models
   config = {
       "model_type": "llama",
       "hidden_size": 4096,
       "num_attention_heads": 32,
       # ... other parameters
   }
   ```

3. **Use Hugging Face integration**:
   - Load via Hugging Face model ID
   - Automatic config and tokenizer download
   - Cached local copies

### Problem: Safetensors performance issues

**Symptoms**:
- Slow tensor loading
- High memory usage during loading
- GPU memory allocation failures

**Solutions**:

1. **Optimize loading**:
   ```python
   # Use device mapping for large models
   device_map = "auto"  # or specific GPU mapping
   ```

2. **Memory management**:
   - Use torch.cuda.empty_cache() between loads
   - Enable gradient checkpointing
   - Use mixed precision (fp16/bf16)

3. **Streaming loading**:
   - Load tensors progressively
   - Use memory mapping
   - Implement lazy loading

## PyTorch Bin Format Issues

### Problem: PyTorch bin files fail to load

**Symptoms**:
- "Cannot load PyTorch model" error
- "Pickle loading failed" message
- Security warnings about pickle files

**Solutions**:

1. **Security considerations**:
   ```python
   # Only load trusted PyTorch files
   # Consider using safetensors instead
   import torch
   torch.serialization.add_safe_globals(['your_trusted_classes'])
   ```

2. **Check PyTorch version compatibility**:
   ```bash
   python -c "import torch; print(torch.__version__)"
   # Ensure compatibility with model's PyTorch version
   ```

3. **Use transformers backend**:
   - PyTorch bin files work with transformers
   - Ensure proper model class detection
   - Check for custom model implementations

4. **File structure validation**:
   - Ensure pytorch_model.bin exists
   - Check for config.json
   - Verify tokenizer files

### Problem: PyTorch model directory structure

**Symptoms**:
- "Model directory incomplete" error
- Missing configuration files
- Tokenizer not found

**Solutions**:

1. **Complete model directory**:
   ```
   model_directory/
   ├── pytorch_model.bin (or model.safetensors)
   ├── config.json
   ├── tokenizer.json
   ├── tokenizer_config.json
   └── vocab.txt (or equivalent)
   ```

2. **Download missing files**:
   - Use Hugging Face hub to download complete model
   - Check model card for required files
   - Use git-lfs for large files

3. **Manual file creation**:
   - Create minimal config.json if missing
   - Use generic tokenizer for testing
   - Provide fallback configurations

### Problem: PyTorch model conversion needed

**Symptoms**:
- "Model format not supported" error
- Custom model architectures
- Non-standard implementations

**Solutions**:

1. **Convert to standard format**:
   ```python
   # Convert custom model to Hugging Face format
   from transformers import AutoModel, AutoTokenizer
   
   # Load custom model
   model = YourCustomModel.load_pretrained("path")
   
   # Save in standard format
   model.save_pretrained("converted_model")
   ```

2. **Use model adapters**:
   - Create adapter for custom architectures
   - Implement standard interfaces
   - Register custom model classes

3. **Alternative loading methods**:
   - Try different transformers model classes
   - Use AutoModel for automatic detection
   - Check for community converters

## Hugging Face Model Issues

### Problem: Hugging Face model download fails

**Symptoms**:
- "Model not found" error
- Authentication failures
- Network timeout errors

**Solutions**:

1. **Verify model ID**:
   ```python
   from huggingface_hub import model_info
   try:
       info = model_info("microsoft/DialoGPT-medium")
       print("Model exists and is accessible")
   except Exception as e:
       print(f"Model issue: {e}")
   ```

2. **Authentication setup**:
   ```bash
   # Install huggingface_hub
   pip install huggingface_hub
   
   # Login with token
   huggingface-cli login
   ```

3. **Network and proxy issues**:
   ```python
   # Configure proxy if needed
   import os
   os.environ['HTTP_PROXY'] = 'http://proxy:port'
   os.environ['HTTPS_PROXY'] = 'https://proxy:port'
   ```

4. **Alternative download methods**:
   - Use git clone with git-lfs
   - Download via browser and load locally
   - Use mirror repositories

### Problem: Hugging Face authentication

**Symptoms**:
- "Authentication required" error
- Private model access denied
- Token validation failures

**Solutions**:

1. **Token management**:
   ```python
   from huggingface_hub import login
   login(token="your_token_here")
   
   # Or set environment variable
   import os
   os.environ['HUGGINGFACE_HUB_TOKEN'] = 'your_token'
   ```

2. **Token permissions**:
   - Ensure token has read permissions
   - Check token expiration
   - Verify model access permissions

3. **Organization access**:
   - Request access to private models
   - Check organization membership
   - Use organization tokens if required

### Problem: Hugging Face model caching

**Symptoms**:
- Repeated downloads
- Cache corruption
- Disk space issues

**Solutions**:

1. **Cache management**:
   ```python
   from huggingface_hub import scan_cache_dir
   
   # Check cache status
   cache_info = scan_cache_dir()
   print(f"Cache size: {cache_info.size_on_disk_str}")
   
   # Clean cache if needed
   cache_info.delete_revisions(*cache_info.repos[0].revisions).execute()
   ```

2. **Custom cache location**:
   ```python
   import os
   os.environ['HUGGINGFACE_HUB_CACHE'] = '/path/to/custom/cache'
   ```

3. **Offline mode**:
   ```python
   # Use cached models only
   os.environ['TRANSFORMERS_OFFLINE'] = '1'
   ```

## Cross-Format Issues

### Problem: Format detection fails

**Symptoms**:
- "Unknown format" error
- Wrong backend selected
- Format misidentification

**Solutions**:

1. **Manual format specification**:
   ```python
   from app.services.universal_model_loader import UniversalModelLoader
   loader = UniversalModelLoader()
   result = loader.load_model("model_path", format_hint="gguf")
   ```

2. **Check file extensions**:
   - Ensure proper file extensions (.gguf, .safetensors, .bin)
   - Rename files if necessary
   - Check for hidden extensions

3. **Directory structure analysis**:
   - For multi-file models, ensure complete directory
   - Check for indicator files (config.json, etc.)
   - Verify file permissions

### Problem: Backend routing issues

**Symptoms**:
- Wrong backend selected for format
- Backend conflicts
- Performance degradation

**Solutions**:

1. **Check backend availability**:
   ```python
   from app.core.backend_routing_system import BackendRoutingSystem
   router = BackendRoutingSystem()
   available = router.get_available_backends()
   print(f"Available backends: {available}")
   ```

2. **Manual backend selection**:
   ```python
   # Force specific backend
   result = loader.load_model("model_path", backend_hint="transformers")
   ```

3. **Backend priority configuration**:
   ```json
   {
     "backend_priorities": {
       "gguf": ["llama_cpp_python", "llamafile"],
       "safetensors": ["transformers"],
       "pytorch_bin": ["transformers"]
     }
   }
   ```

## Backend Selection Issues

### Problem: No suitable backend found

**Symptoms**:
- "No compatible backend" error
- All backends fail
- Missing dependencies

**Solutions**:

1. **Install missing backends**:
   ```bash
   # Install all supported backends
   pip install transformers torch
   pip install llama-cpp-python
   pip install ctransformers
   ```

2. **Check backend requirements**:
   ```python
   from app.core.backend_routing_system import BackendRoutingSystem
   router = BackendRoutingSystem()
   requirements = router.check_backend_requirements()
   print(requirements)
   ```

3. **Fallback options**:
   - Enable CPU-only mode
   - Use alternative model formats
   - Try different quantization levels

### Problem: Backend performance issues

**Symptoms**:
- Slow model loading
- Poor inference performance
- Memory issues

**Solutions**:

1. **Backend optimization**:
   ```python
   # Get optimization recommendations
   from app.core.enhanced_memory_manager import EnhancedMemoryManager
   memory_manager = EnhancedMemoryManager()
   suggestions = memory_manager.suggest_memory_optimizations(model_info, available_memory)
   ```

2. **Hardware-specific tuning**:
   - GPU layer optimization
   - Memory mapping configuration
   - Thread count adjustment

3. **Performance monitoring**:
   ```python
   # Monitor backend performance
   from app.core.enhanced_error_reporting import EnhancedErrorReporting
   reporter = EnhancedErrorReporting()
   performance_report = reporter.generate_performance_report()
   ```

## General Troubleshooting Tips

### Diagnostic Commands

1. **Check system compatibility**:
   ```python
   from app.core.universal_format_detector import UniversalFormatDetector
   detector = UniversalFormatDetector()
   system_info = detector.get_system_compatibility()
   print(system_info)
   ```

2. **Test all backends**:
   ```python
   from app.core.backend_routing_system import BackendRoutingSystem
   router = BackendRoutingSystem()
   test_results = router.test_all_backends()
   print(test_results)
   ```

3. **Memory analysis**:
   ```python
   from app.core.enhanced_memory_manager import EnhancedMemoryManager
   memory_manager = EnhancedMemoryManager()
   memory_report = memory_manager.get_memory_analysis()
   print(memory_report)
   ```

### Prevention Tips

1. **Keep dependencies updated**:
   ```bash
   pip install --upgrade transformers torch safetensors huggingface_hub
   ```

2. **Regular cache cleanup**:
   - Clear Hugging Face cache periodically
   - Remove unused model files
   - Monitor disk space

3. **Backup configurations**:
   - Save working backend configurations
   - Document successful model loading settings
   - Keep notes on format-specific issues

### Getting Help

When reporting format-specific issues, include:

1. **Model information**:
   - Format type and version
   - File size and source
   - Model architecture if known

2. **System details**:
   - Operating system and version
   - Python and package versions
   - Available memory and GPU

3. **Error details**:
   - Complete error messages
   - Steps to reproduce
   - Attempted solutions

4. **Diagnostic output**:
   - Format detection results
   - Backend availability
   - Memory analysis

For additional help:
- Check the main [Troubleshooting Guide](troubleshooting_guide.md)
- Visit the [User Guide](user_guide.md) for basic usage
- Report issues on GitHub with diagnostic information