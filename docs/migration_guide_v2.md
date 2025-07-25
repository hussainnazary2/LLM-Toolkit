# Migration Guide: GGUF Loader to llm toolkit v2.0

This guide helps users migrate from the original GGUF Loader application to llm toolkit v2.0 with universal model format support.

## Table of Contents

1. [What's New in v2.0](#whats-new-in-v20)
2. [Breaking Changes](#breaking-changes)
3. [Migration Steps](#migration-steps)
4. [Configuration Migration](#configuration-migration)
5. [Model File Compatibility](#model-file-compatibility)
6. [New Features Guide](#new-features-guide)
7. [Troubleshooting Migration Issues](#troubleshooting-migration-issues)

## What's New in v2.0

### Universal Model Format Support

llm toolkit v2.0 expands beyond GGUF files to support:

- **GGUF files**: Full backward compatibility with existing GGUF models
- **Safetensors**: Secure tensor format support
- **PyTorch models**: Direct loading of `.bin` files and model directories
- **Hugging Face integration**: Load models directly by ID from Hugging Face Hub

### Intelligent Backend System

- **Automatic format detection**: No need to specify model format
- **Smart backend selection**: Optimal backend chosen based on format and hardware
- **Fallback mechanisms**: Automatic retry with alternative backends on failure
- **Performance optimization**: Hardware-aware configuration tuning

### Enhanced User Experience

- **Unified interface**: Same clean interface for all model formats
- **Better error reporting**: Detailed, actionable error messages
- **Memory management**: Improved memory usage and optimization suggestions
- **Progress tracking**: Better feedback during model loading and downloads

## Breaking Changes

### Configuration Directory

**Old location**: `~/.gguf-loader/`
**New location**: `~/.llm-toolkit/`

The application will automatically migrate your configuration on first run.

### Command Line Arguments

**Old**: `--model path/to/model.gguf`
**New**: `--model path/to/model` (supports all formats and HF model IDs)

### API Changes (for addon developers)

Some internal APIs have been updated to support multiple formats:

```python
# Old API
from app.models.gguf_model import GGUFModel
model = GGUFModel("model.gguf")

# New API
from app.services.universal_model_loader import UniversalModelLoader
loader = UniversalModelLoader()
result = await loader.load_model("model.gguf")  # or any supported format
```

### Backend Configuration

Backend configuration format has been updated to support multiple formats:

```json
// Old format
{
  "backend": "llama_cpp_python",
  "gpu_layers": -1
}

// New format
{
  "backends": {
    "llama_cpp_python": {
      "gpu_layers": -1,
      "supported_formats": ["gguf"]
    },
    "transformers": {
      "device_map": "auto",
      "supported_formats": ["safetensors", "pytorch_bin", "huggingface"]
    }
  }
}
```

## Migration Steps

### Step 1: Backup Your Data

Before upgrading, backup your important data:

```bash
# Backup configuration
cp -r ~/.gguf-loader ~/.gguf-loader-backup

# Backup any custom addons
cp -r /path/to/gguf-loader-app/addons /path/to/backup/addons

# Note down your current settings
```

### Step 2: Install llm toolkit v2.0

1. **Download** the new version
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application** for the first time

### Step 3: Automatic Configuration Migration

On first run, llm toolkit will:

1. **Detect old configuration** in `~/.gguf-loader/`
2. **Migrate settings** to `~/.llm-toolkit/`
3. **Update backend configurations** to new format
4. **Preserve addon settings** and preferences

### Step 4: Verify Migration

1. **Check settings**: Go to Settings → Preferences to verify your settings
2. **Test model loading**: Load a GGUF model to ensure backward compatibility
3. **Verify addons**: Check that your addons are working correctly
4. **Test new features**: Try loading a Hugging Face model

### Step 5: Clean Up (Optional)

After verifying everything works:

```bash
# Remove old configuration directory
rm -rf ~/.gguf-loader

# Remove old application directory if desired
```

## Configuration Migration

### Settings Migration

The following settings are automatically migrated:

| Old Setting | New Setting | Notes |
|-------------|-------------|-------|
| `backend_preference` | `backends.default` | Updated to new format |
| `gpu_layers` | `backends.llama_cpp_python.gpu_layers` | Moved to backend-specific config |
| `theme` | `ui.theme` | Preserved as-is |
| `model_directory` | `paths.model_directory` | Preserved as-is |
| `addon_settings` | `addons` | Preserved with compatibility updates |

### Manual Configuration Updates

Some settings may require manual updates:

#### Backend Preferences

**Old configuration**:
```json
{
  "backend": "llama_cpp_python",
  "gpu_layers": 32,
  "context_size": 2048
}
```

**New configuration**:
```json
{
  "backends": {
    "default": "auto",
    "llama_cpp_python": {
      "gpu_layers": 32,
      "context_size": 2048,
      "priority": 1
    },
    "transformers": {
      "device_map": "auto",
      "priority": 2
    }
  }
}
```

#### Model Paths

Update any hardcoded paths in scripts or configurations:

```bash
# Old paths
~/.gguf-loader/models/
~/.gguf-loader/cache/

# New paths
~/.llm-toolkit/models/
~/.llm-toolkit/cache/
```

## Model File Compatibility

### GGUF Files

**Full backward compatibility**: All existing GGUF files work without changes.

- Same loading process
- Same performance characteristics
- All quantization levels supported
- Existing model metadata preserved

### New Format Support

You can now also load:

#### Safetensors Files

```python
# Example: Loading a safetensors model
loader = UniversalModelLoader()
result = await loader.load_model("model.safetensors")
```

#### PyTorch Models

```python
# Example: Loading a PyTorch model directory
result = await loader.load_model("/path/to/pytorch_model/")
```

#### Hugging Face Models

```python
# Example: Loading from Hugging Face Hub
result = await loader.load_model("microsoft/DialoGPT-medium")
```

### Model Organization

Consider organizing your models by format:

```
models/
├── gguf/
│   ├── llama-7b-q4_0.gguf
│   └── mistral-7b-q8_0.gguf
├── safetensors/
│   ├── model1.safetensors
│   └── model2.safetensors
├── pytorch/
│   ├── model1/
│   └── model2/
└── huggingface_cache/
    └── (automatically managed)
```

## New Features Guide

### Hugging Face Integration

1. **Set up authentication** (for private models):
   - Settings → Hugging Face → Authentication
   - Enter your HF token

2. **Load models by ID**:
   - File → Load Model → Hugging Face Model
   - Enter model ID (e.g., `gpt2`, `microsoft/DialoGPT-small`)

3. **Manage cached models**:
   - Settings → Hugging Face → Cache Management

### Format Detection

The system automatically detects model formats:

- **File extension**: `.gguf`, `.safetensors`, `.bin`
- **Directory structure**: PyTorch model directories
- **Model ID pattern**: Hugging Face model IDs
- **File headers**: Binary format identification

### Backend Selection

The system chooses optimal backends automatically:

- **GGUF → llama-cpp-python/llamafile**
- **Safetensors → transformers**
- **PyTorch → transformers**
- **Hugging Face → transformers**

### Enhanced Error Reporting

New error messages provide:

- **Root cause analysis**
- **Actionable solutions**
- **Alternative suggestions**
- **Format-specific guidance**

## Troubleshooting Migration Issues

### Configuration Migration Failed

**Symptoms**: Settings not preserved, default configuration loaded

**Solutions**:
1. **Manual migration**:
   ```bash
   cp ~/.gguf-loader/config.json ~/.llm-toolkit/config.json
   ```
2. **Reset and reconfigure**:
   - Delete `~/.llm-toolkit/`
   - Restart application
   - Reconfigure manually

### Models Not Loading

**Symptoms**: Previously working GGUF models fail to load

**Solutions**:
1. **Check backend availability**:
   - Settings → Diagnostics → Backend Test
   - Reinstall backends if needed

2. **Try manual backend selection**:
   ```python
   result = await loader.load_model("model.gguf", backend_hint="llama_cpp_python")
   ```

3. **Check file permissions**:
   ```bash
   ls -la /path/to/model.gguf
   chmod 644 /path/to/model.gguf
   ```

### Addon Compatibility Issues

**Symptoms**: Addons not working or showing errors

**Solutions**:
1. **Check addon compatibility**:
   - Look for v2.0 compatible versions
   - Check addon documentation

2. **Update addon interfaces**:
   ```python
   # Old interface
   from app.models.gguf_model import GGUFModel
   
   # New interface
   from app.services.universal_model_loader import UniversalModelLoader
   ```

3. **Contact addon developers** for v2.0 updates

### Performance Issues

**Symptoms**: Slower model loading or inference

**Solutions**:
1. **Check backend selection**:
   - Verify optimal backend is chosen
   - Try manual backend specification

2. **Update hardware drivers**:
   - GPU drivers
   - CUDA/ROCm versions

3. **Clear caches**:
   ```bash
   rm -rf ~/.llm-toolkit/cache/
   ```

### New Format Issues

**Symptoms**: Safetensors or PyTorch models not loading

**Solutions**:
1. **Install required dependencies**:
   ```bash
   pip install safetensors transformers torch
   ```

2. **Check format detection**:
   ```python
   from app.core.universal_format_detector import UniversalFormatDetector
   detector = UniversalFormatDetector()
   result = detector.detect_format("your_model")
   print(result.format_type)
   ```

3. **Try manual format specification**:
   ```python
   result = await loader.load_model("model", format_hint="safetensors")
   ```

## Getting Help

### Migration Support

If you encounter issues during migration:

1. **Check logs**: `~/.llm-toolkit/logs/migration.log`
2. **Enable debug mode**: `python main.py --debug`
3. **Consult documentation**:
   - [Format-Specific Troubleshooting](format_troubleshooting.md)
   - [Hugging Face Integration Guide](huggingface_guide.md)
   - [Developer Guide](developer_guide_multiformat.md)

### Community Support

- **GitHub Issues**: Report migration problems
- **Discussions**: Ask questions about new features
- **Discord**: Real-time help from community

### Rollback Instructions

If you need to rollback to the old version:

1. **Restore backup**:
   ```bash
   rm -rf ~/.llm-toolkit
   mv ~/.gguf-loader-backup ~/.gguf-loader
   ```

2. **Reinstall old version**
3. **Report issues** to help improve the migration process

## Post-Migration Checklist

- [ ] Configuration migrated successfully
- [ ] Existing GGUF models load correctly
- [ ] Addons working properly
- [ ] New format support tested
- [ ] Hugging Face integration configured (if needed)
- [ ] Performance acceptable
- [ ] Backup of old configuration removed
- [ ] Documentation bookmarked for reference

Welcome to llm toolkit v2.0! The universal model loading capabilities open up access to thousands of additional models while maintaining full backward compatibility with your existing GGUF collection.