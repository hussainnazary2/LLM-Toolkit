# Hugging Face Integration Guide

This guide covers how to use llm toolkit's Hugging Face integration to load models directly from the Hugging Face Hub.

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Authentication](#authentication)
4. [Loading Models](#loading-models)
5. [Model Management](#model-management)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

## Overview

llm toolkit's Hugging Face integration allows you to:

- Load models directly by Hugging Face model ID
- Automatically download and cache models locally
- Handle authentication for private models
- Manage model versions and updates
- Access thousands of pre-trained models

### Supported Model Types

The integration works with models that are compatible with the transformers library:
- Text generation models (GPT, LLaMA, Mistral, etc.)
- Conversational models (DialoGPT, BlenderBot, etc.)
- Instruction-tuned models (Alpaca, Vicuna, etc.)
- Code generation models (CodeT5, StarCoder, etc.)

## Getting Started

### Prerequisites

1. **Install required packages** (automatically handled by llm toolkit):
   ```bash
   pip install transformers huggingface_hub torch
   ```

2. **Internet connection** for initial model downloads

3. **Sufficient disk space** for model caching

### Basic Usage

1. **Open llm toolkit**
2. **Go to File → Load Model**
3. **Select "Hugging Face Model ID" option**
4. **Enter a model ID** (e.g., `microsoft/DialoGPT-medium`)
5. **Click Load** and wait for download and loading

### Quick Start Example

Try loading a small conversational model:
```
Model ID: microsoft/DialoGPT-small
```

This model is relatively small (~117MB) and good for testing the integration.

## Authentication

### When Authentication is Needed

Authentication is required for:
- Private models and datasets
- Models from private organizations
- Rate-limited API access
- Accessing gated models (some require approval)

### Setting Up Authentication

#### Method 1: Through llm toolkit UI

1. **Go to Settings → Hugging Face → Authentication**
2. **Enter your Hugging Face token**
3. **Click "Validate Token"** to test
4. **Save settings**

#### Method 2: Command Line Setup

```bash
# Install huggingface_hub if not already installed
pip install huggingface_hub

# Login with your token
huggingface-cli login
```

#### Method 3: Environment Variable

```bash
# Set environment variable
export HUGGINGFACE_HUB_TOKEN="your_token_here"

# On Windows
set HUGGINGFACE_HUB_TOKEN=your_token_here
```

### Getting a Hugging Face Token

1. **Visit** [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. **Click "New token"**
3. **Choose token type**:
   - **Read**: For downloading public and private models
   - **Write**: For uploading models (not needed for llm toolkit)
4. **Copy the token** and save it securely
5. **Use the token** in llm toolkit authentication

### Token Management

#### Validating Your Token

```python
from huggingface_hub import whoami

try:
    user_info = whoami()
    print(f"Logged in as: {user_info['name']}")
    print(f"Token is valid")
except Exception as e:
    print(f"Token validation failed: {e}")
```

#### Token Permissions

Ensure your token has appropriate permissions:
- **Read access** to repositories you want to access
- **Organization membership** for private org models
- **Gated model approval** if accessing restricted models

## Loading Models

### By Model ID

The most common way to load Hugging Face models:

1. **Find a model** on [Hugging Face Hub](https://huggingface.co/models)
2. **Copy the model ID** (format: `username/model-name`)
3. **In llm toolkit**:
   - File → Load Model
   - Select "Hugging Face Model ID"
   - Enter the model ID
   - Click Load

### Popular Model IDs to Try

#### Small Models (Good for Testing)
```
microsoft/DialoGPT-small          # 117MB - Conversational
distilgpt2                        # 319MB - Text generation
gpt2                              # 548MB - Text generation
```

#### Medium Models
```
microsoft/DialoGPT-medium         # 345MB - Conversational
gpt2-medium                       # 1.52GB - Text generation
facebook/blenderbot-400M-distill  # 400MB - Conversational
```

#### Large Models (Require More Memory)
```
microsoft/DialoGPT-large          # 1.38GB - Conversational
gpt2-large                        # 3.16GB - Text generation
facebook/blenderbot-1B-distill    # 1GB - Conversational
```

### Loading Process

When you load a Hugging Face model:

1. **Model ID Validation**: Checks if the model exists and is accessible
2. **Download Progress**: Shows download progress for model files
3. **Caching**: Stores downloaded files locally for future use
4. **Loading**: Loads the model into memory using the transformers backend
5. **Ready**: Model is ready for chat or text generation

### Download Progress

During download, you'll see:
- **File names** being downloaded
- **Progress bars** for each file
- **Total download size** and progress
- **Estimated time remaining**

## Model Management

### Local Cache

Downloaded models are cached locally to avoid re-downloading:

#### Cache Location
- **Windows**: `C:\Users\{username}\.cache\huggingface\hub`
- **macOS**: `~/.cache/huggingface/hub`
- **Linux**: `~/.cache/huggingface/hub`

#### Cache Management

1. **View cache usage**:
   ```python
   from huggingface_hub import scan_cache_dir
   
   cache_info = scan_cache_dir()
   print(f"Cache size: {cache_info.size_on_disk_str}")
   print(f"Number of repos: {len(cache_info.repos)}")
   ```

2. **Clean cache** (in llm toolkit):
   - Settings → Hugging Face → Cache Management
   - View cached models
   - Delete unused models
   - Clear entire cache if needed

### Model Updates

Hugging Face models can be updated by their authors:

#### Checking for Updates

llm toolkit automatically checks for updates when loading cached models:
- **Green indicator**: Model is up to date
- **Yellow indicator**: Update available
- **Red indicator**: Model has been removed or access revoked

#### Updating Models

1. **Automatic updates**: Enable in Settings → Hugging Face → Auto-update
2. **Manual updates**: 
   - Right-click cached model
   - Select "Check for updates"
   - Download updates if available

### Model Information

View detailed information about Hugging Face models:

1. **Model card**: Automatically downloaded and displayed
2. **Model architecture**: Detected from config.json
3. **Model size**: File sizes and parameter count
4. **License information**: Usage restrictions and permissions
5. **Performance metrics**: If available from model card

## Advanced Features

### Custom Cache Directory

Set a custom location for model caching:

```python
import os
os.environ['HUGGINGFACE_HUB_CACHE'] = '/path/to/custom/cache'
```

Or in llm toolkit:
- Settings → Hugging Face → Cache Directory
- Browse to desired location
- Restart application

### Offline Mode

Use only cached models without internet access:

```python
import os
os.environ['TRANSFORMERS_OFFLINE'] = '1'
```

Or in llm toolkit:
- Settings → Hugging Face → Offline Mode
- Enable offline mode
- Only cached models will be available

### Model Variants

Some models have multiple variants (different sizes, quantizations):

```
# Different sizes of the same model
gpt2                    # 124M parameters
gpt2-medium            # 355M parameters  
gpt2-large             # 774M parameters
gpt2-xl                # 1.5B parameters

# Different quantizations
microsoft/DialoGPT-medium
microsoft/DialoGPT-medium-fp16
```

### Private Models

Loading private models requires authentication:

1. **Ensure authentication** is set up
2. **Request access** if model is gated
3. **Load normally** using model ID
4. **Handle access errors** if permissions insufficient

### Organization Models

Models from organizations may require special access:

```
# Organization model format
organization-name/model-name

# Examples
huggingface/CodeBERTa-small-v1
microsoft/DialoGPT-medium
facebook/blenderbot-400M-distill
```

## Troubleshooting

### Common Issues

#### "Model not found" Error

**Causes**:
- Typo in model ID
- Model doesn't exist
- Model is private and you lack access

**Solutions**:
1. **Verify model ID** on Hugging Face website
2. **Check spelling** and capitalization
3. **Ensure authentication** for private models
4. **Request access** for gated models

#### Authentication Failures

**Symptoms**:
- "Authentication required" error
- "Invalid token" message
- Access denied for private models

**Solutions**:
1. **Check token validity**:
   ```bash
   huggingface-cli whoami
   ```
2. **Regenerate token** if expired
3. **Verify token permissions**
4. **Check organization membership**

#### Download Failures

**Symptoms**:
- Network timeout errors
- Partial downloads
- Corrupted files

**Solutions**:
1. **Check internet connection**
2. **Retry download** (llm toolkit auto-retries)
3. **Clear cache** and re-download
4. **Use VPN** if region-blocked
5. **Check firewall settings**

#### Memory Issues

**Symptoms**:
- Out of memory errors
- System becomes unresponsive
- Model loading fails

**Solutions**:
1. **Choose smaller models** for testing
2. **Close other applications**
3. **Use CPU-only mode** if GPU memory insufficient
4. **Enable memory optimization** in settings

### Diagnostic Commands

#### Check Model Accessibility

```python
from huggingface_hub import model_info

try:
    info = model_info("microsoft/DialoGPT-medium")
    print(f"Model: {info.modelId}")
    print(f"Downloads: {info.downloads}")
    print(f"Tags: {info.tags}")
except Exception as e:
    print(f"Error: {e}")
```

#### Test Authentication

```python
from huggingface_hub import whoami

try:
    user = whoami()
    print(f"Authenticated as: {user['name']}")
except Exception as e:
    print(f"Authentication failed: {e}")
```

#### Check Cache Status

```python
from huggingface_hub import scan_cache_dir

cache = scan_cache_dir()
print(f"Cache location: {cache.cache_dir}")
print(f"Total size: {cache.size_on_disk_str}")

for repo in cache.repos:
    print(f"Repo: {repo.repo_id}")
    print(f"Size: {repo.size_on_disk_str}")
```

## Best Practices

### Model Selection

1. **Start small**: Test with small models first
2. **Check requirements**: Verify memory and compute needs
3. **Read model cards**: Understand intended use and limitations
4. **Consider licenses**: Ensure compliance with usage terms

### Performance Optimization

1. **Use appropriate hardware**: GPU for large models, CPU for small ones
2. **Monitor memory usage**: Keep track of system resources
3. **Cache management**: Regularly clean unused models
4. **Batch processing**: Load multiple models efficiently

### Security Considerations

1. **Verify model sources**: Only use trusted models
2. **Check model cards**: Look for safety information
3. **Sandbox testing**: Test new models in isolated environment
4. **Token security**: Keep authentication tokens secure

### Storage Management

1. **Monitor cache size**: Large models consume significant space
2. **Regular cleanup**: Remove unused cached models
3. **Custom cache location**: Use dedicated storage if needed
4. **Backup important models**: Save frequently used models

### Network Efficiency

1. **Batch downloads**: Download multiple models when network is available
2. **Offline preparation**: Pre-download models for offline use
3. **Resume capability**: Use tools that support resume on failure
4. **Mirror usage**: Use regional mirrors when available

## Integration with llm toolkit Features

### Chat Functionality

Hugging Face models work seamlessly with llm toolkit's chat features:
- **System prompts**: Set custom instructions
- **Temperature control**: Adjust response creativity
- **Max tokens**: Limit response length
- **Conversation history**: Maintain context across messages

### Model Comparison

Compare different Hugging Face models:
1. **Load multiple models** from different sources
2. **Test same prompts** across models
3. **Compare performance** and quality
4. **Document results** for future reference

### Addon Integration

Hugging Face models work with llm toolkit addons:
- **Email assistant**: Use for email generation
- **Code helper**: Use code-specific models
- **Translation**: Use multilingual models
- **Summarization**: Use models optimized for summarization

## Support and Resources

### Documentation
- [Hugging Face Hub Documentation](https://huggingface.co/docs/hub/)
- [Transformers Documentation](https://huggingface.co/docs/transformers/)
- [Model Hub](https://huggingface.co/models)

### Community
- [Hugging Face Forums](https://discuss.huggingface.co/)
- [Discord Community](https://discord.gg/JfAtkvEtRb)
- [GitHub Issues](https://github.com/huggingface/transformers/issues)

### Getting Help

When seeking help with Hugging Face integration:

1. **Include model ID** you're trying to load
2. **Provide error messages** in full
3. **Share system information** (OS, memory, etc.)
4. **Describe steps taken** to reproduce issue
5. **Include authentication status** (without sharing tokens)

For llm toolkit-specific issues:
- Check the [Format Troubleshooting Guide](format_troubleshooting.md)
- Visit the main [Troubleshooting Guide](troubleshooting_guide.md)
- Report issues on the llm toolkit GitHub repository