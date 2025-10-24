# Migration Guide

## Overview

This guide helps existing GGUF Loader App users migrate from the legacy llama-cpp-python backend to the new multi-backend system. The migration process is designed to be seamless while providing improved reliability, performance, and GPU support.

## Pre-Migration Checklist

### Backup Current Setup

Before starting the migration, backup your current configuration:

```bash
# Create backup directory
mkdir ~/.gguf-loader-backup

# Backup configuration files
cp ~/.gguf-loader/config.json ~/.gguf-loader-backup/
cp -r ~/.gguf-loader/models/ ~/.gguf-loader-backup/models/
cp -r ~/.gguf-loader/logs/ ~/.gguf-loader-backup/logs/

# Backup application settings (Windows)
reg export "HKEY_CURRENT_USER\Software\GGUFLoader" ~/.gguf-loader-backup/registry.reg

# Note current model paths and settings
echo "Current models:" > ~/.gguf-loader-backup/current_setup.txt
ls ~/.gguf-loader/models/ >> ~/.gguf-loader-backup/current_setup.txt
```

### Document Current Performance

Record baseline performance metrics for comparison:

```python
# Run this before migration
from app.core.benchmark import ModelBenchmark

benchmark = ModelBenchmark()
baseline = benchmark.run_comprehensive_test()

# Save results
with open('~/.gguf-loader-backup/baseline_performance.json', 'w') as f:
    json.dump(baseline, f, indent=2)
```

### System Requirements Check

Verify your system meets requirements for new backends:

```python
from app.core.system_checker import SystemChecker

checker = SystemChecker()
compatibility = checker.check_backend_compatibility()

print("Backend Compatibility:")
for backend, status in compatibility.items():
    print(f"  {backend}: {'✓' if status.compatible else '✗'}")
    if not status.compatible:
        print(f"    Issues: {', '.join(status.issues)}")
```

## Migration Process

### Step 1: Update Application

1. **Download Latest Version**:
   - Download from GitHub releases
   - Or update via package manager
   - Verify version includes backend system

2. **Install New Dependencies**:
   ```bash
   # Update pip and install new requirements
   pip install --upgrade pip
   pip install -r requirements.txt
   
   # Install recommended backend
   pip install ctransformers[cuda]  # For NVIDIA GPUs
   pip install ctransformers[rocm]  # For AMD GPUs
   pip install ctransformers        # CPU only
   ```

3. **Verify Installation**:
   ```python
   # Test new backend system
   from app.core.backend_manager import BackendManager
   
   manager = BackendManager()
   available = manager.detect_available_backends()
   print(f"Available backends: {available}")
   ```

### Step 2: Configuration Migration

The application automatically migrates most settings, but you can also migrate manually:

#### Automatic Migration

On first startup with the new version:

1. **Configuration Detection**:
   - App detects existing configuration
   - Prompts for migration confirmation
   - Creates backup of old config

2. **Settings Translation**:
   ```json
   // Old configuration
   {
     "model_path": "/path/to/model.gguf",
     "n_gpu_layers": 35,
     "n_ctx": 2048,
     "n_batch": 512,
     "use_mlock": true
   }
   
   // New configuration
   {
     "preferred_backend": "ctransformers",
     "model_path": "/path/to/model.gguf",
     "backends": {
       "ctransformers": {
         "gpu_layers": 35,
         "context_size": 2048,
         "batch_size": 512,
         "use_mlock": true
       }
     }
   }
   ```

3. **Model Registry Update**:
   - Existing model paths preserved
   - Model metadata updated
   - Performance history maintained

#### Manual Migration

If automatic migration fails or you prefer manual control:

1. **Create New Configuration**:
   ```bash
   # Copy template configuration
   cp ~/.gguf-loader/config_template.json ~/.gguf-loader/config.json
   ```

2. **Transfer Settings**:
   ```python
   # Migration script
   from app.core.config_migrator import ConfigMigrator
   
   migrator = ConfigMigrator()
   migrator.migrate_from_legacy('~/.gguf-loader-backup/config.json')
   ```

3. **Validate Configuration**:
   ```python
   from app.core.config_validator import ConfigValidator
   
   validator = ConfigValidator()
   result = validator.validate_config('~/.gguf-loader/config.json')
   
   if not result.valid:
       print("Configuration issues:")
       for issue in result.issues:
           print(f"  - {issue}")
   ```

### Step 3: Backend Selection

Choose the optimal backend for your system:

#### Automatic Selection

Let the system choose the best backend:

```python
from app.core.backend_selector import BackendSelector

selector = BackendSelector()
recommendation = selector.get_recommendation()

print(f"Recommended backend: {recommendation.backend}")
print(f"Reason: {recommendation.reason}")
print(f"Expected performance: {recommendation.performance_estimate}")
```

#### Manual Selection

Choose based on your specific needs:

**For NVIDIA GPU Users**:
```json
{
  "preferred_backend": "ctransformers",
  "backends": {
    "ctransformers": {
      "enabled": true,
      "gpu_layers": -1,
      "gpu_enabled": true
    }
  }
}
```

**For AMD GPU Users**:
```json
{
  "preferred_backend": "transformers",
  "backends": {
    "transformers": {
      "enabled": true,
      "device_map": "auto",
      "torch_dtype": "float16"
    }
  }
}
```

**For CPU-Only Users**:
```json
{
  "preferred_backend": "llamafile",
  "backends": {
    "llamafile": {
      "enabled": true,
      "threads": 8,
      "use_mmap": true
    }
  }
}
```

### Step 4: Model Testing

Test your existing models with the new backend:

#### Quick Test

```python
from app.models.gguf_model import GGUFModel

# Test model loading
model = GGUFModel()
result = model.load('/path/to/your/model.gguf')

if result.success:
    print(f"Model loaded successfully with {result.backend}")
    print(f"Load time: {result.load_time:.2f}s")
    print(f"Memory usage: {result.memory_usage}MB")
else:
    print(f"Loading failed: {result.error}")
```

#### Comprehensive Test

```python
from app.core.model_tester import ModelTester

tester = ModelTester()
results = tester.test_all_models()

for model_path, result in results.items():
    print(f"\nModel: {model_path}")
    print(f"  Status: {'✓' if result.success else '✗'}")
    print(f"  Backend: {result.backend}")
    print(f"  Performance: {result.tokens_per_second:.1f} tok/s")
    
    if not result.success:
        print(f"  Error: {result.error}")
        print(f"  Suggested fix: {result.suggestion}")
```

### Step 5: Performance Comparison

Compare performance before and after migration:

```python
from app.core.performance_comparer import PerformanceComparer

comparer = PerformanceComparer()
comparison = comparer.compare_with_baseline('~/.gguf-loader-backup/baseline_performance.json')

print("Performance Comparison:")
print(f"  Loading time: {comparison.loading_time_change:+.1f}%")
print(f"  Inference speed: {comparison.inference_speed_change:+.1f}%")
print(f"  Memory usage: {comparison.memory_usage_change:+.1f}%")
print(f"  GPU utilization: {comparison.gpu_utilization_change:+.1f}%")

if comparison.overall_improvement > 0:
    print(f"\n✓ Overall performance improved by {comparison.overall_improvement:.1f}%")
else:
    print(f"\n⚠ Performance decreased by {abs(comparison.overall_improvement):.1f}%")
    print("Consider trying a different backend or adjusting settings")
```

## Common Migration Scenarios

### Scenario 1: NVIDIA GPU User with Working llama-cpp-python

**Current Setup**:
- NVIDIA RTX 3080 (10GB VRAM)
- llama-cpp-python with CUDA
- 13B model with Q4_0 quantization

**Migration Steps**:

1. **Install ctransformers**:
   ```bash
   pip install ctransformers[cuda]
   ```

2. **Configure for similar performance**:
   ```json
   {
     "preferred_backend": "ctransformers",
     "backends": {
       "ctransformers": {
         "gpu_layers": -1,
         "context_size": 2048,
         "batch_size": 512
       }
     }
   }
   ```

3. **Expected improvements**:
   - Faster loading times
   - More stable GPU utilization
   - Better error handling

### Scenario 2: User with Installation Issues

**Current Setup**:
- NVIDIA GPU but llama-cpp-python won't install
- Compilation errors with CUDA
- Currently using CPU-only mode

**Migration Steps**:

1. **Try ctransformers first**:
   ```bash
   pip install ctransformers[cuda]
   ```

2. **If that fails, try transformers**:
   ```bash
   pip install transformers accelerate torch
   ```

3. **Fallback to llamafile**:
   ```bash
   # Download llamafile executable
   wget https://github.com/Mozilla-Ocho/llamafile/releases/latest/download/llamafile
   chmod +x llamafile
   ```

4. **Configure fallback chain**:
   ```json
   {
     "fallback_enabled": true,
     "fallback_order": ["ctransformers", "transformers", "llamafile"]
   }
   ```

### Scenario 3: AMD GPU User

**Current Setup**:
- AMD RX 6800 XT
- llama-cpp-python with ROCm (if working)
- Looking for better AMD support

**Migration Steps**:

1. **Install transformers with ROCm**:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.4.2
   pip install transformers accelerate
   ```

2. **Configure for AMD**:
   ```json
   {
     "preferred_backend": "transformers",
     "backends": {
       "transformers": {
         "device_map": "auto",
         "torch_dtype": "float16"
       }
     }
   }
   ```

3. **Alternative with ctransformers**:
   ```bash
   pip install ctransformers[rocm]
   ```

### Scenario 4: macOS Apple Silicon User

**Current Setup**:
- MacBook Pro M2 Max
- llama-cpp-python with Metal
- Good performance but want reliability

**Migration Steps**:

1. **Install ctransformers**:
   ```bash
   pip install ctransformers
   ```

2. **Configure for Metal**:
   ```json
   {
     "preferred_backend": "ctransformers",
     "backends": {
       "ctransformers": {
         "gpu_layers": -1,
         "metal_enabled": true
       }
     }
   }
   ```

3. **Alternative with transformers**:
   ```bash
   pip install transformers accelerate torch
   ```

## Troubleshooting Migration Issues

### Configuration Migration Fails

**Symptoms**:
- App won't start after update
- Configuration errors on startup
- Settings not preserved

**Solutions**:

1. **Reset to defaults**:
   ```bash
   mv ~/.gguf-loader/config.json ~/.gguf-loader/config.json.broken
   # App will create new default config
   ```

2. **Manual configuration**:
   ```python
   from app.core.config_manager import ConfigManager
   
   config = ConfigManager()
   config.reset_to_defaults()
   config.set_backend('ctransformers')
   config.save()
   ```

3. **Restore from backup**:
   ```bash
   cp ~/.gguf-loader-backup/config.json ~/.gguf-loader/config.json
   # Then run migration tool
   ```

### Backend Installation Issues

**Symptoms**:
- No backends available
- Installation errors
- Import failures

**Solutions**:

1. **Check Python environment**:
   ```bash
   python --version  # Should be 3.8-3.11
   pip list | grep -E "(torch|transformers|ctransformers)"
   ```

2. **Clean installation**:
   ```bash
   pip uninstall ctransformers transformers torch
   pip cache purge
   pip install ctransformers[cuda]
   ```

3. **Use virtual environment**:
   ```bash
   python -m venv gguf_new_env
   source gguf_new_env/bin/activate  # Linux/Mac
   gguf_new_env\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

### Performance Regression

**Symptoms**:
- Slower than before migration
- Higher memory usage
- Poor GPU utilization

**Solutions**:

1. **Try different backend**:
   ```python
   # Test all available backends
   from app.core.backend_tester import BackendTester
   
   tester = BackendTester()
   results = tester.benchmark_all_backends()
   
   best_backend = max(results.items(), key=lambda x: x[1].performance)
   print(f"Best backend: {best_backend[0]}")
   ```

2. **Optimize configuration**:
   ```python
   from app.core.config_optimizer import ConfigOptimizer
   
   optimizer = ConfigOptimizer()
   optimal_config = optimizer.optimize_for_hardware()
   optimizer.apply_config(optimal_config)
   ```

3. **Check hardware utilization**:
   ```bash
   # Monitor during inference
   nvidia-smi dmon -s pucvmet -d 1  # NVIDIA
   rocm-smi --showuse --showmemuse  # AMD
   ```

### Model Compatibility Issues

**Symptoms**:
- Models won't load
- Format not supported errors
- Conversion required messages

**Solutions**:

1. **Check model format**:
   ```python
   from app.core.model_inspector import ModelInspector
   
   inspector = ModelInspector()
   info = inspector.inspect_model('/path/to/model.gguf')
   
   print(f"Format: {info.format}")
   print(f"Compatible backends: {info.compatible_backends}")
   ```

2. **Try different backend**:
   ```python
   # Some backends handle different formats better
   backends_to_try = ['ctransformers', 'transformers', 'llamafile']
   
   for backend in backends_to_try:
       try:
           model.load_with_backend(model_path, backend)
           print(f"Success with {backend}")
           break
       except Exception as e:
           print(f"Failed with {backend}: {e}")
   ```

3. **Model conversion**:
   ```python
   from app.core.model_converter import ModelConverter
   
   converter = ModelConverter()
   if converter.needs_conversion(model_path):
       converted_path = converter.convert_model(model_path)
       model.load(converted_path)
   ```

## Post-Migration Optimization

### Fine-Tuning Performance

After successful migration, optimize for your specific use case:

1. **Run optimization wizard**:
   ```python
   from app.core.optimization_wizard import OptimizationWizard
   
   wizard = OptimizationWizard()
   recommendations = wizard.analyze_usage_patterns()
   wizard.apply_recommendations(recommendations)
   ```

2. **Monitor and adjust**:
   ```python
   from app.core.performance_monitor import PerformanceMonitor
   
   monitor = PerformanceMonitor()
   monitor.start_continuous_monitoring()
   
   # After a week of usage
   insights = monitor.get_optimization_insights()
   print("Optimization suggestions:")
   for suggestion in insights.suggestions:
       print(f"  - {suggestion}")
   ```

### Updating Documentation

Update your personal documentation:

1. **Document new configuration**:
   ```bash
   # Save current working configuration
   cp ~/.gguf-loader/config.json ~/my_gguf_config_backup.json
   
   # Document performance baselines
   echo "Post-migration performance:" >> ~/gguf_migration_notes.txt
   # Add benchmark results
   ```

2. **Create troubleshooting notes**:
   ```bash
   echo "Working configuration for my system:" > ~/gguf_troubleshooting.txt
   echo "Backend: ctransformers" >> ~/gguf_troubleshooting.txt
   echo "GPU layers: -1" >> ~/gguf_troubleshooting.txt
   echo "Batch size: 512" >> ~/gguf_troubleshooting.txt
   ```

## Rollback Procedure

If migration causes issues and you need to rollback:

### Quick Rollback

1. **Restore configuration**:
   ```bash
   cp ~/.gguf-loader-backup/config.json ~/.gguf-loader/config.json
   ```

2. **Reinstall old backend**:
   ```bash
   pip uninstall ctransformers transformers
   pip install llama-cpp-python
   ```

3. **Restore application version**:
   - Download previous version
   - Or use git to revert changes

### Complete Rollback

1. **Restore entire directory**:
   ```bash
   rm -rf ~/.gguf-loader
   cp -r ~/.gguf-loader-backup ~/.gguf-loader
   ```

2. **Restore system settings**:
   ```bash
   # Windows
   reg import ~/.gguf-loader-backup/registry.reg
   
   # Linux/Mac
   # Restore any system-level configurations
   ```

3. **Verify functionality**:
   ```python
   # Test that everything works as before
   from app.models.gguf_model import GGUFModel
   
   model = GGUFModel()
   result = model.load('/path/to/test/model.gguf')
   print(f"Rollback successful: {result.success}")
   ```

## Support and Resources

### Getting Help

If you encounter issues during migration:

1. **Check migration logs**:
   ```bash
   tail -f ~/.gguf-loader/logs/migration.log
   ```

2. **Run diagnostic tool**:
   ```python
   from app.core.migration_diagnostics import MigrationDiagnostics
   
   diagnostics = MigrationDiagnostics()
   report = diagnostics.generate_report()
   print(report)
   ```

3. **Contact support**:
   - GitHub Issues with migration label
   - Include diagnostic report
   - Specify your hardware and OS

### Additional Resources

- [Backend System Documentation](backend_system.md)
- [Troubleshooting Guide](troubleshooting_guide.md)
- [Performance Optimization](performance_optimization.md)
- [Hardware Compatibility](hardware_compatibility.md)

### Community

- Discord: Real-time migration help
- Reddit: Community experiences and tips
- GitHub Discussions: Detailed technical questions
- Wiki: Community-contributed guides

## Migration Success Checklist

- [ ] Backup created successfully
- [ ] New version installed and working
- [ ] At least one backend available
- [ ] Configuration migrated correctly
- [ ] All models load successfully
- [ ] Performance meets or exceeds baseline
- [ ] GPU acceleration working (if applicable)
- [ ] Error handling improved
- [ ] Documentation updated
- [ ] Rollback procedure tested (optional)

Congratulations on successfully migrating to the new backend system! You should now have improved reliability, better GPU support, and easier troubleshooting capabilities.