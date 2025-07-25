# llm toolkit User Guide

Welcome to llm toolkit! This guide will help you get started with using the application's clean, minimal interface for AI-powered tasks with universal model format support.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Interface Overview](#interface-overview)
3. [Loading Models](#loading-models)
4. [Chat Functionality](#chat-functionality)
5. [Document Summarization](#document-summarization)
6. [Menu System](#menu-system)
7. [Addon Management](#addon-management)
8. [Settings and Preferences](#settings-and-preferences)
9. [Troubleshooting](#troubleshooting)
10. [Tips and Best Practices](#tips-and-best-practices)

## Getting Started

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **Memory**: 8GB RAM minimum (16GB recommended for larger models)
- **Storage**: 2GB free space (plus space for GGUF models)

### Installation

1. **Download** llm toolkit from the official repository
2. **Extract** the files to your desired location
3. **Install dependencies** by running:
   ```bash
   pip install -r requirements.txt
   ```
4. **Launch** the application:
   ```bash
   python main.py
   ```

### First Launch

When you first launch the application, you'll see a clean, minimal interface with:
- A model selection dropdown at the top (initially empty)
- Two main tabs: **Chat** and **Summarization**
- A comprehensive menu bar for advanced settings
- A status bar showing application status

## Interface Overview

llm toolkit features a **clean, distraction-free interface** with only essential controls visible on the main surface. Advanced settings and configurations are organized in the menu system.

### Main Components

#### 1. Model Selection Bar
- Located at the top of the window
- Shows currently loaded model (if any)
- Click to select from available models
- Displays model status and memory usage

#### 2. Tab System
- **Chat Tab**: For conversational AI interactions
- **Summarization Tab**: For document processing and summarization
- Clean tab switching with no clutter

#### 3. Menu Bar
- **File**: Model loading, recent files, document operations
- **Edit**: Copy/paste, preferences, settings
- **Model**: AI parameters, system prompts, model configuration
- **Addons**: Addon management, installation, configuration
- **Help**: Documentation, about information

#### 4. Status Bar
- Shows current model status
- Displays memory usage (unobtrusive)
- Connection status and background operations

## Loading Models

### Supported Formats

llm toolkit supports **all major AI model formats**:
- **GGUF files**: `.gguf` files with quantized models (Q4_0, Q4_1, Q8_0, etc.)
- **Safetensors**: `.safetensors` files for secure tensor storage
- **PyTorch models**: `.bin` files and model directories with `pytorch_model.bin`
- **Hugging Face models**: Direct loading by model ID (e.g., `microsoft/DialoGPT-medium`)
- Various model architectures (LLaMA, Mistral, GPT, BERT, etc.)

### Loading a Model

#### Method 1: File Menu
1. Go to **File → Load Model**
2. Choose your loading method:
   - **Browse Files**: Select `.gguf`, `.safetensors`, or `.bin` files
   - **Browse Directory**: Select PyTorch model directories
   - **Hugging Face ID**: Enter model ID (e.g., `microsoft/DialoGPT-medium`)
3. Wait for the model to load (progress shown in status bar)
4. Model appears in the selection dropdown when ready

#### Method 2: Drag and Drop
1. Simply drag a model file or directory into the application window
2. The system automatically detects the format
3. The model will begin loading with the optimal backend
4. Loading progress is shown in the status bar

#### Method 3: Hugging Face Integration
1. Go to **File → Load Model → Hugging Face Model**
2. Enter a model ID (e.g., `gpt2`, `microsoft/DialoGPT-small`)
3. The model downloads and caches automatically
4. Authentication is handled if needed for private models

#### Method 3: Recent Models
1. Go to **File → Recent Models**
2. Select from previously loaded models
3. Model loads quickly if still in memory

### Model Information

Once a model is loaded, you can view its information:
- **Model → Model Information** shows detailed metadata
- Status bar displays current memory usage
- Model dropdown shows model name and status

## Chat Functionality

The Chat tab provides a clean interface for conversational AI interactions.

### Basic Chat

1. **Select the Chat tab** (if not already active)
2. **Type your message** in the input area at the bottom
3. **Press Enter** or click **Send** to submit
4. **AI response** appears in the conversation area
5. **Continue the conversation** naturally

### Chat Features

#### Message History
- All messages in the current session are preserved
- Scroll up to view previous exchanges
- Clear conversation via **Edit → Clear Chat**

#### Visual Design
- **User messages**: Aligned to the right with distinct styling
- **AI responses**: Aligned to the left with different styling
- **Timestamps**: Subtle timestamps for each message
- **Progress indicators**: Shown while AI is generating responses

#### Advanced Options (via Menu)
- **Model → System Prompt**: Set custom system instructions
- **Model → Temperature**: Adjust response creativity (0.0-1.0)
- **Model → Max Tokens**: Limit response length
- **Model → Generation Parameters**: Fine-tune AI behavior

### Chat Tips

- **Be specific** in your questions for better responses
- **Use system prompts** to set the AI's role or behavior
- **Adjust temperature** for more creative (higher) or focused (lower) responses
- **Clear conversation** when switching topics for better context

## Document Summarization

The Summarization tab provides tools for processing and summarizing documents.

### Text Summarization

1. **Select the Summarization tab**
2. **Enter or paste text** in the input area
3. **Choose summarization style**:
   - **Concise**: Brief, key points only
   - **Detailed**: Comprehensive summary
   - **Bullet Points**: Structured list format
4. **Click Summarize** to process
5. **Review the summary** in the output area

### File Summarization

1. **Click "Load File"** in the Summarization tab
2. **Select a supported file**:
   - Text files (`.txt`)
   - Markdown files (`.md`)
   - PDF files (`.pdf`)
   - Word documents (`.docx`)
3. **Choose summarization options**
4. **Process the file** and review results

### Summarization Options

#### Style Options
- **Concise**: 2-3 sentences, main points only
- **Detailed**: Paragraph-length, comprehensive
- **Bullet Points**: Structured list of key points
- **Executive Summary**: Business-focused overview

#### Length Control
- **Short**: ~100 words
- **Medium**: ~250 words
- **Long**: ~500 words
- **Custom**: Specify exact word count

### Working with Results

- **Copy to Clipboard**: Click the copy button
- **Save to File**: Use **File → Save Summary**
- **Edit Summary**: Make manual adjustments
- **Re-summarize**: Try different styles or lengths

## Menu System

All advanced settings and configurations are organized in the menu system to keep the main interface clean.

### File Menu

#### Model Operations
- **Load Model**: Browse and load GGUF files
- **Recent Models**: Quick access to previously loaded models
- **Model Information**: View detailed model metadata
- **Unload Model**: Free memory by unloading current model

#### Document Operations
- **Open Document**: Load files for summarization
- **Save Chat**: Export chat conversation
- **Save Summary**: Export summarization results
- **Recent Documents**: Quick access to recent files

#### Application
- **Preferences**: Open settings dialog
- **Exit**: Close the application

### Edit Menu

#### Standard Operations
- **Copy**: Copy selected text
- **Paste**: Paste from clipboard
- **Select All**: Select all text in current area
- **Find**: Search within conversations or documents

#### Conversation Management
- **Clear Chat**: Clear current conversation
- **Clear Summary**: Clear summarization results
- **Reset Session**: Start fresh with current model

#### Settings
- **Preferences**: Open detailed settings dialog
- **Keyboard Shortcuts**: View and customize shortcuts

### Model Menu

#### AI Configuration
- **System Prompt**: Set custom system instructions
- **Temperature**: Adjust response creativity (0.0-1.0)
- **Max Tokens**: Set maximum response length
- **Top-P**: Configure nucleus sampling
- **Repetition Penalty**: Reduce repetitive responses

#### Model Management
- **Model Parameters**: View and adjust model settings
- **Memory Usage**: Monitor and optimize memory usage
- **Performance Settings**: Configure for your hardware

### Addons Menu

#### Addon Management
- **Manage Addons**: View installed addons and their status
- **Install Addon**: Add new addons to the application
- **Browse Addons**: Discover available addons
- **Addon Settings**: Configure individual addon preferences

#### Installed Addons
- Each installed addon may add its own menu items here
- Examples: "Email Assistant", "Finance Advisor", "Code Helper"

### Help Menu

#### Documentation
- **User Guide**: This guide
- **Addon Development**: Guide for creating addons
- **API Reference**: Technical documentation
- **Keyboard Shortcuts**: List of all shortcuts

#### Support
- **About**: Application version and information
- **Check for Updates**: Update the application
- **Report Issue**: Submit bug reports or feedback
- **Community**: Links to user community and support

## Addon Management

The GGUF Loader App supports powerful addons that extend functionality while maintaining the clean interface.

### Viewing Installed Addons

1. Go to **Addons → Manage Addons**
2. View list of installed addons with status
3. See addon information, version, and description
4. Enable/disable addons as needed

### Installing New Addons

#### From File
1. **Addons → Install Addon**
2. **Browse** for addon file (`.zip` or folder)
3. **Install** and restart if required
4. **Enable** the addon in the management interface

#### From Repository
1. **Addons → Browse Addons**
2. **Search** available addons
3. **Install** directly from the repository
4. **Configure** addon settings if needed

### Popular Addons

#### Email Automation
- AI-powered email response generation
- Template management
- Integration with email clients
- Access via **Addons → Email Assistant**

#### Finance Assistant
- Budget analysis and planning
- Investment advice and analysis
- Financial document processing
- Access via **Addons → Finance Advisor**

#### Theme Customization
- Custom color schemes
- Interface layout options
- Font and sizing preferences
- Access via **Edit → Preferences → Themes**

### Addon Configuration

1. **Addons → Manage Addons**
2. **Select an addon** from the list
3. **Click Configure** to access settings
4. **Adjust preferences** as needed
5. **Apply changes** and restart if required

## Settings and Preferences

Access comprehensive settings through **Edit → Preferences** or **File → Preferences**.

### General Settings

#### Interface
- **Theme**: Light, Dark, or System
- **Font Size**: Adjust text size throughout the app
- **Window Behavior**: Minimize to tray, remember size/position
- **Language**: Interface language selection

#### Performance
- **Memory Management**: Automatic cleanup settings
- **Background Processing**: Enable/disable background operations
- **Hardware Acceleration**: GPU utilization settings
- **Model Caching**: Cache frequently used models

### AI Settings

#### Default Parameters
- **System Prompt**: Default instructions for AI
- **Temperature**: Default creativity level (0.0-1.0)
- **Max Tokens**: Default response length limit
- **Model Directory**: Default location for GGUF files

#### Chat Settings
- **Message History**: How many messages to remember
- **Auto-save Conversations**: Automatically save chat sessions
- **Response Formatting**: How AI responses are displayed
- **Typing Indicators**: Show when AI is generating responses

#### Summarization Settings
- **Default Style**: Preferred summarization approach
- **Default Length**: Preferred summary length
- **File Processing**: How different file types are handled
- **Output Format**: How summaries are formatted

### Advanced Settings

#### Logging
- **Log Level**: Debug, Info, Warning, Error
- **Log Location**: Where log files are stored
- **Log Retention**: How long to keep log files

#### Network
- **Proxy Settings**: Configure proxy if needed
- **Update Checking**: Automatic update preferences
- **Telemetry**: Usage data collection preferences

#### Security
- **Model Validation**: Verify model integrity
- **Addon Security**: Sandbox addon execution
- **Data Privacy**: Local processing preferences

## Troubleshooting

### Common Issues

#### Model Loading Problems

**Problem**: Model fails to load
**Solutions**:
- Check file integrity (re-download if corrupted)
- Ensure sufficient memory (close other applications)
- Verify GGUF format compatibility
- Check file permissions

**Problem**: Model loads but responses are poor
**Solutions**:
- Adjust temperature settings (**Model → Temperature**)
- Modify system prompt (**Model → System Prompt**)
- Check model quantization level
- Try different generation parameters

#### Performance Issues

**Problem**: Application runs slowly
**Solutions**:
- Close unused models (**File → Unload Model**)
- Reduce max tokens (**Model → Max Tokens**)
- Enable hardware acceleration (**Edit → Preferences → Performance**)
- Increase system memory

**Problem**: High memory usage
**Solutions**:
- Use smaller/quantized models
- Enable automatic memory cleanup
- Unload models when not needed
- Monitor usage in status bar

#### Interface Issues

**Problem**: UI elements not responding
**Solutions**:
- Restart the application
- Check for addon conflicts (**Addons → Manage Addons**)
- Reset preferences (**Edit → Preferences → Reset**)
- Update to latest version

### Getting Help

#### Built-in Help
- **Help → User Guide**: This comprehensive guide
- **Help → Keyboard Shortcuts**: Quick reference
- **Help → About**: Version and system information

#### Community Support
- **Help → Community**: Access user forums and discussions
- **Help → Report Issue**: Submit bug reports with logs
- **GitHub Repository**: Source code and issue tracking

#### Logs and Diagnostics
- **View → Show Logs**: Access application logs
- **Help → System Information**: Detailed system diagnostics
- **Debug Mode**: Enable via command line for detailed logging

## Tips and Best Practices

### Model Management

#### Choosing Models
- **Smaller models** (7B parameters) for faster responses
- **Larger models** (13B+ parameters) for better quality
- **Quantized models** (Q4, Q8) for memory efficiency
- **Specialized models** for specific tasks

#### Memory Optimization
- **Unload unused models** to free memory
- **Use quantized versions** when possible
- **Monitor memory usage** in the status bar
- **Close other applications** when using large models

### Chat Best Practices

#### Effective Prompting
- **Be specific** about what you want
- **Provide context** for better responses
- **Use examples** to clarify your request
- **Break complex tasks** into smaller parts

#### System Prompts
- **Set role-specific prompts** for different tasks
- **Include formatting instructions** for consistent output
- **Specify tone and style** preferences
- **Update prompts** for different conversation types

### Summarization Tips

#### Input Preparation
- **Clean up text** before summarization
- **Remove irrelevant sections** for better focus
- **Use appropriate file formats** for best results
- **Consider document structure** when choosing styles

#### Output Optimization
- **Try different styles** for various needs
- **Adjust length** based on use case
- **Edit summaries** for final polish
- **Save templates** for repeated use

### Addon Usage

#### Selection Criteria
- **Choose reputable addons** from trusted sources
- **Read reviews and documentation** before installing
- **Test in safe environment** before production use
- **Keep addons updated** for security and compatibility

#### Performance Impact
- **Disable unused addons** to improve performance
- **Monitor resource usage** of active addons
- **Configure addon settings** for optimal performance
- **Report issues** to addon developers

### Workflow Optimization

#### Keyboard Shortcuts
- **Learn common shortcuts** for faster operation
- **Customize shortcuts** for your workflow
- **Use menu mnemonics** for quick access
- **Practice shortcuts** to build muscle memory

#### Session Management
- **Save important conversations** before closing
- **Use multiple tabs** for different tasks
- **Organize models** in dedicated folders
- **Backup settings** and preferences regularly

### Security and Privacy

#### Data Protection
- **Keep models local** for sensitive data
- **Review addon permissions** before installation
- **Use secure file storage** for important documents
- **Regular backups** of conversations and settings

#### Model Security
- **Verify model sources** before downloading
- **Scan files** for malware before loading
- **Use official repositories** when possible
- **Keep application updated** for security patches

---

This user guide provides comprehensive information for getting the most out of the GGUF Loader App's clean, efficient interface. For additional help, consult the built-in help system or visit the community forums.

---

This user guide provides comprehensive information for getting the most out of llm toolkit's clean, efficient interface with universal model format support. For additional help, consult the built-in help system or visit the community forums.

**Version**: 2.0.0  
**Last Updated**: 2024  
**For Technical Support**: See Help → Community or Help → Report Issue

## Additional Resources

- **[Format-Specific Troubleshooting](format_troubleshooting.md)** - Detailed troubleshooting for each supported format
- **[Hugging Face Integration Guide](huggingface_guide.md)** - Complete guide for using Hugging Face models
- **[Migration Guide](migration_guide_v2.md)** - Upgrading from GGUF Loader to llm toolkit
- **[Developer Documentation](developer_guide_multiformat.md)** - Technical documentation for developers