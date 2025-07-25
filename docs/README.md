# llm toolkit Documentation

Welcome to the llm toolkit documentation. This directory contains comprehensive guides for users and developers working with the universal AI model loading system.

## Documentation Index

### For Users

- **[User Guide](user_guide.md)** - Complete guide for using the application
  - Getting started and installation
  - Interface overview and navigation
  - Loading and managing AI models (GGUF, safetensors, PyTorch, Hugging Face)
  - Universal model format support
  - Chat functionality and best practices
  - Document summarization features
  - Menu system and settings
  - Addon management and usage
  - Troubleshooting and tips

- **[Format-Specific Troubleshooting](format_troubleshooting.md)** - Troubleshooting for all supported formats
  - GGUF format issues and solutions
  - Safetensors format troubleshooting
  - PyTorch bin file problems
  - Hugging Face integration issues
  - Cross-format compatibility

- **[Hugging Face Integration Guide](huggingface_guide.md)** - Complete guide for Hugging Face Hub integration
  - Authentication and token management
  - Loading models by ID
  - Model caching and management
  - Private model access
  - Troubleshooting download issues

### Backend System Documentation

- **[Backend System](backend_system.md)** - Comprehensive backend system documentation
  - Architecture overview and supported backends
  - Hardware detection and optimization
  - Configuration management
  - Performance monitoring and diagnostics

- **[Troubleshooting Guide](troubleshooting_guide.md)** - Solutions for common issues
  - GPU detection and installation problems
  - Backend-specific troubleshooting
  - Performance optimization tips
  - System-specific solutions

- **[Performance Optimization](performance_optimization.md)** - Performance tuning guide
  - Hardware-specific optimizations
  - Model and quantization selection
  - Backend configuration tuning
  - System-level optimizations

- **[Migration Guide](migration_guide.md)** - Migration from legacy backends
  - Pre-migration preparation
  - Step-by-step migration process
  - Common migration scenarios
  - Troubleshooting migration issues

- **[v2.0 Migration Guide](migration_guide_v2.md)** - Upgrading from GGUF Loader to llm toolkit
  - What's new in v2.0 (universal format support)
  - Breaking changes and compatibility
  - Step-by-step migration process
  - Configuration updates and new features

- **[Hardware Compatibility](hardware_compatibility.md)** - Hardware support information
  - GPU compatibility matrix
  - System requirements
  - Performance expectations
  - Hardware recommendations

### For Addon Developers

- **[Addon Development Guide](addon_development.md)** - Complete guide for creating addons
  - Getting started with addon development
  - Interface implementations
  - UI extensions
  - Multi-format model support in addons
  - Example addons
  - Best practices and troubleshooting

- **[API Reference](api_reference.md)** - Quick reference for all interfaces
  - Core interfaces (IAddon, IAddonService)
  - Service interfaces (IModelService, IChatService, ISummarizationService)
  - Extension interfaces (IUIExtension, IModelProcessor, IModelProvider)
  - Multi-format model interfaces
  - Data classes and enums
  - Usage examples

- **[Multi-Format Developer Guide](developer_guide_multiformat.md)** - Technical guide for multi-format system
  - Architecture overview and design principles
  - Core components (format detection, backend routing, validation)
  - Metadata extraction and memory management
  - Error reporting framework
  - Extension points for new formats and backends
  - Testing framework and performance considerations

### For Core Developers

- **[Event Bus Documentation](event_bus.md)** - Internal event system documentation
- **[Testing Guide](testing_guide.md)** - Comprehensive testing framework documentation
  - Testing framework overview
  - Running tests and test configurations
  - Writing unit, UI, and addon tests
  - Performance and memory testing
  - Test utilities and best practices
  - Continuous integration setup

## Quick Start for Addon Development

1. **Read the basics**: Start with the [Addon Development Guide](addon_development.md)
2. **Check the API**: Use the [API Reference](api_reference.md) for quick lookups
3. **Study examples**: Look at the sample addons in the `addons/` directory
4. **Test your addon**: Follow the testing guidelines in the development guide

## Interface Overview

llm toolkit provides several interfaces for addon integration with universal model format support:

### Core Interfaces
- `IAddon` - Main addon interface (required)
- `IAddonService` - Backend service access

### Service Interfaces
- `IModelService` - Direct model operations
- `IChatService` - Chat functionality
- `ISummarizationService` - Document processing

### Extension Interfaces
- `IUIExtension` - UI extensions
- `IModelProcessor` - Custom model processing
- `IModelProvider` - Custom model loading

## Getting Help

- Check the troubleshooting section in the [Addon Development Guide](addon_development.md)
- Review the example addons for implementation patterns
- Use the [API Reference](api_reference.md) for interface details

## Contributing

When contributing to the documentation:

1. Keep examples simple and focused
2. Include error handling in code samples
3. Update the API reference when interfaces change
4. Test all code examples before committing

## Version Information

This documentation is for llm toolkit version 2.0.0 and later, featuring universal model format support.
Check the interface compatibility in your addon metadata.