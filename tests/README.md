# Comprehensive Test Suite for Reliable GPU Backend System

This directory contains a comprehensive test suite for the reliable GPU backend system, covering all aspects of backend functionality, performance, and hardware compatibility.

## Test Structure

```
tests/
├── unit/                    # Unit tests for individual components
│   ├── test_backend_interfaces.py      # Backend abstraction layer tests
│   ├── test_backend_implementations.py # Individual backend tests
│   ├── test_hardware_detector.py       # Hardware detection tests
│   └── test_backend_manager.py         # Backend manager tests
├── integration/             # Integration tests for complex scenarios
│   └── test_backend_switching.py       # Backend switching and fallback tests
├── performance/             # Performance benchmarking tests
│   └── test_backend_benchmarks.py      # Performance comparison tests
├── mock/                    # Mock tests for various hardware configurations
│   └── test_hardware_scenarios.py      # Different hardware scenario tests
├── conftest.py             # Shared fixtures and configuration
├── test_runner.py          # Main test runner script
└── README.md               # This file
```

## Test Categories

### 1. Unit Tests (`tests/unit/`)

Tests individual components in isolation:

- **Backend Interfaces** (`test_backend_interfaces.py`)
  - BackendConfig data structure validation
  - HardwareInfo serialization/deserialization
  - LoadingResult and GenerationConfig functionality
  - BackendRegistry operations
  - Abstract ModelBackend class behavior

- **Backend Implementations** (`test_backend_implementations.py`)
  - CtransformersBackend functionality
  - TransformersBackend functionality
  - LlamafileBackend functionality
  - LlamaCppPythonBackend functionality
  - Model loading, text generation, and unloading

- **Hardware Detector** (`test_hardware_detector.py`)
  - GPU detection (NVIDIA, AMD, Intel)
  - CPU information detection
  - System memory detection
  - Hardware optimization recommendations
  - Benchmarking capabilities

- **Backend Manager** (`test_backend_manager.py`)
  - Backend lifecycle management
  - Configuration management
  - Performance monitoring integration
  - Statistics and reporting

### 2. Integration Tests (`tests/integration/`)

Tests complex interactions between components:

- **Backend Switching** (`test_backend_switching.py`)
  - Seamless backend switching with model reload
  - Fallback chain execution when backends fail
  - Configuration persistence across switches
  - Performance monitoring during switches
  - Error handling and recovery scenarios

### 3. Performance Tests (`tests/performance/`)

Benchmarks and performance analysis:

- **Backend Benchmarks** (`test_backend_benchmarks.py`)
  - Model loading time comparisons
  - Text generation speed measurements
  - Memory usage pattern analysis
  - Resource utilization tracking
  - Scalability under load testing
  - Long-running stability tests

### 4. Mock Tests (`tests/mock/`)

Tests behavior across different hardware configurations:

- **Hardware Scenarios** (`test_hardware_scenarios.py`)
  - High-end gaming systems (RTX 4090, 32GB RAM)
  - Mid-range systems (GTX 1660, 16GB RAM)
  - Budget systems (integrated graphics, 8GB RAM)
  - Server systems (multiple A100s, 512GB RAM)
  - Apple Silicon systems (M1/M2 with unified memory)
  - AMD GPU systems (RX 7900 XTX with ROCm)
  - CPU-only systems
  - Memory-constrained systems (4GB RAM)

## Running Tests

### Quick Start

```bash
# Run all unit and integration tests
python tests/test_runner.py

# Run specific test category
python tests/test_runner.py unit
python tests/test_runner.py integration
python tests/test_runner.py performance
python tests/test_runner.py mock

# Run all tests
python tests/test_runner.py all
```

### Advanced Usage

```bash
# Verbose output
python tests/test_runner.py -v

# Skip slow tests
python tests/test_runner.py --fast

# Only GPU-required tests
python tests/test_runner.py --gpu-required

# Quick smoke tests
python tests/test_runner.py --smoke

# Generate coverage report
python tests/test_runner.py --coverage
```

### Using pytest directly

```bash
# Run specific test file
pytest tests/unit/test_backend_interfaces.py -v

# Run tests with specific marker
pytest -m unit -v
pytest -m "performance and not slow" -v

# Run with coverage
pytest --cov=core --cov=backends --cov-report=html
```

## Test Markers

Tests are categorized using pytest markers:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests  
- `@pytest.mark.performance` - Performance tests
- `@pytest.mark.mock` - Mock hardware tests
- `@pytest.mark.slow` - Tests that take a long time
- `@pytest.mark.gpu_required` - Tests requiring actual GPU

## Fixtures and Test Data

### Common Fixtures (`conftest.py`)

- `temp_dir` - Temporary directory for test files
- `mock_model_file` - Small mock GGUF model file
- `large_mock_model_file` - Large mock model file (100MB)
- `backend_config` - Default backend configuration
- `generation_config` - Default generation configuration
- `mock_hardware_detector` - Mock hardware detector with realistic data
- `mock_backend_factory` - Factory for creating mock backends
- `performance_test_data` - Test prompts for performance testing
- `benchmark_configs` - Different generation configurations for benchmarking

### Hardware Scenarios

- `mock_gpu_device` - Mock NVIDIA GPU device
- `mock_hardware_info` - Standard hardware configuration
- `cpu_only_hardware_info` - CPU-only system
- `amd_gpu_hardware_info` - AMD GPU system
- `multi_gpu_hardware_info` - Multi-GPU system

## Test Requirements

### Dependencies

```bash
pip install pytest pytest-cov pytest-mock pytest-timeout
```

### Optional Dependencies for Performance Tests

```bash
pip install pytest-benchmark memory-profiler
```

### Mock Dependencies

All backend dependencies are mocked in tests, so you don't need to install:
- ctransformers
- transformers
- torch
- llama-cpp-python

## Coverage Goals

The test suite aims for:
- **90%+ code coverage** across all core modules
- **100% coverage** of critical paths (model loading, generation, error handling)
- **Comprehensive scenario coverage** across different hardware configurations

## Continuous Integration

The test suite is designed to run in CI environments:

```yaml
# Example GitHub Actions workflow
- name: Run comprehensive tests
  run: |
    python tests/test_runner.py unit integration --fast
    
- name: Run performance benchmarks
  run: |
    python tests/test_runner.py performance --fast
    
- name: Generate coverage report
  run: |
    python tests/test_runner.py unit --coverage
```

## Contributing

When adding new functionality:

1. **Add unit tests** for new components
2. **Add integration tests** for complex interactions
3. **Add performance tests** for performance-critical code
4. **Add mock tests** for hardware-specific behavior
5. **Update fixtures** if new test data is needed
6. **Run full test suite** before submitting changes

### Test Writing Guidelines

- Use descriptive test names that explain what is being tested
- Follow the Arrange-Act-Assert pattern
- Mock external dependencies appropriately
- Test both success and failure scenarios
- Include edge cases and boundary conditions
- Add performance assertions for critical paths
- Use appropriate test markers

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the app directory is in Python path
2. **Mock Failures**: Check that all external dependencies are properly mocked
3. **Timeout Errors**: Increase timeout for slow tests or mark them as `@pytest.mark.slow`
4. **Coverage Issues**: Ensure all code paths are tested, especially error conditions

### Debug Mode

```bash
# Run with debug output
pytest -v -s --tb=long

# Run single test with debugging
pytest tests/unit/test_backend_interfaces.py::TestBackendConfig::test_backend_config_creation -v -s
```

## Performance Benchmarking

Performance tests provide detailed metrics:

- **Loading Times**: Model loading performance across backends
- **Generation Speed**: Tokens per second for different configurations
- **Memory Usage**: RAM and VRAM utilization patterns
- **Throughput**: Concurrent request handling capacity
- **Scalability**: Performance under increasing load

Results are automatically compared and reported, helping identify performance regressions and optimization opportunities.