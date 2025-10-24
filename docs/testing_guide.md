# Testing Guide

This guide provides comprehensive information about testing the GGUF Loader App, including the testing framework, writing tests, and best practices.

## Table of Contents

1. [Testing Framework Overview](#testing-framework-overview)
2. [Running Tests](#running-tests)
3. [Writing Unit Tests](#writing-unit-tests)
4. [UI Testing](#ui-testing)
5. [Addon Testing](#addon-testing)
6. [Performance Testing](#performance-testing)
7. [Test Utilities](#test-utilities)
8. [Best Practices](#best-practices)
9. [Continuous Integration](#continuous-integration)

## Testing Framework Overview

The GGUF Loader App uses a comprehensive testing framework built on pytest with the following components:

### Core Testing Tools
- **pytest**: Main testing framework
- **pytest-qt**: Qt application testing
- **pytest-cov**: Code coverage reporting
- **pytest-mock**: Enhanced mocking utilities
- **pytest-benchmark**: Performance benchmarking

### Test Organization
```
tests/
├── conftest.py              # Global fixtures and configuration
├── test_framework_validation.py  # Framework validation tests
├── core/                    # Core component tests
├── ui/                      # UI component tests
├── services/                # Service layer tests
├── addons/                  # Addon system tests
├── utils/                   # Test utilities and helpers
└── integration/             # Integration tests
```

### Test Categories
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **UI Tests**: Test user interface components
- **Addon Tests**: Test addon functionality and integration
- **Performance Tests**: Benchmark and memory tests
- **Regression Tests**: Tests for bug fixes

## Running Tests

### Basic Test Execution

#### Run All Tests
```bash
python run_tests.py
```

#### Run Specific Test Categories
```bash
python run_tests.py --unit          # Unit tests only
python run_tests.py --ui            # UI tests only
python run_tests.py --addon         # Addon tests only
python run_tests.py --integration   # Integration tests only
```

#### Run Tests with Markers
```bash
python run_tests.py -m unit         # Tests marked as unit
python run_tests.py -m slow         # Tests marked as slow
python run_tests.py -m performance  # Performance tests
```

### Advanced Test Execution

#### Parallel Execution
```bash
python run_tests.py --parallel      # Run tests in parallel
```

#### Coverage Reporting
```bash
python run_tests.py --html          # Generate HTML coverage report
python run_tests.py --json          # Generate JSON test report
```

#### Headless UI Testing
```bash
python run_tests.py --headless      # Run UI tests without display
```

### Test Suite Runner

Use the comprehensive test suite runner for advanced scenarios:

```bash
# Interactive mode
python run_test_suite.py

# Run specific configuration
python run_test_suite.py unit

# Run multiple configurations
python run_test_suite.py unit ui addon

# List available configurations
python run_test_suite.py --list

# Validate test framework
python run_test_suite.py --validate
```

## Writing Unit Tests

### Basic Unit Test Structure

```python
import pytest
from unittest.mock import MagicMock, patch

# Mark test as unit test
pytestmark = pytest.mark.unit

class TestMyComponent:
    """Test suite for MyComponent."""
    
    def test_initialization(self):
        """Test component initialization."""
        component = MyComponent()
        assert component is not None
        assert component.initialized is False
    
    def test_method_with_mock(self, mock_dependency):
        """Test method with mocked dependency."""
        component = MyComponent(mock_dependency)
        result = component.process_data("test")
        
        assert result == "processed: test"
        mock_dependency.process.assert_called_once_with("test")
    
    @pytest.mark.parametrize("input_value,expected", [
        ("hello", "HELLO"),
        ("world", "WORLD"),
        ("", ""),
    ])
    def test_parametrized(self, input_value, expected):
        """Test with multiple parameter sets."""
        component = MyComponent()
        result = component.uppercase(input_value)
        assert result == expected
```

### Using Fixtures

```python
@pytest.fixture
def sample_component():
    """Create a sample component for testing."""
    component = MyComponent()
    component.initialize()
    yield component
    component.cleanup()

def test_with_fixture(sample_component):
    """Test using a fixture."""
    result = sample_component.get_status()
    assert result == "ready"
```

### Mocking External Dependencies

```python
def test_with_external_service(mock_model_service):
    """Test component that depends on external service."""
    # mock_model_service is provided by conftest.py
    component = MyComponent(mock_model_service)
    
    # Configure mock behavior
    mock_model_service.generate.return_value = "mocked response"
    
    # Test the component
    result = component.process_request("test input")
    
    # Verify interactions
    assert result == "mocked response"
    mock_model_service.generate.assert_called_once_with("test input")
```

## UI Testing

### Basic UI Test Structure

```python
import pytest
from tests.utils.ui_test_utils import UITestCase
from PySide6.QtCore import Qt

# Mark as UI test
pytestmark = pytest.mark.ui

class TestMainWindow(UITestCase):
    """Test suite for MainWindow."""
    
    def test_window_creation(self, main_window):
        """Test main window creation."""
        assert main_window.isVisible()
        assert main_window.windowTitle() == "GGUF Loader App"
    
    def test_button_click(self, main_window):
        """Test button click interaction."""
        # Find button
        button = main_window.findChild(QPushButton, "loadModelButton")
        assert button is not None
        
        # Click button
        self.click_button(button)
        
        # Verify result
        assert main_window.model_loaded is True
    
    def test_text_input(self, main_window):
        """Test text input functionality."""
        # Find text input
        text_input = main_window.findChild(QTextEdit, "chatInput")
        
        # Enter text
        self.enter_text(text_input, "Hello, AI!")
        
        # Verify text was entered
        assert text_input.toPlainText() == "Hello, AI!"
```

### Testing Qt Signals

```python
def test_signal_emission(self, main_window):
    """Test that signals are emitted correctly."""
    with self.wait_for_signal(main_window.modelLoaded, timeout=5000) as signal_args:
        # Trigger action that should emit signal
        main_window.load_model("/path/to/model.gguf")
    
    # Verify signal was emitted with correct arguments
    assert len(signal_args) == 1
    assert signal_args[0] == "/path/to/model.gguf"
```

### Testing Dialogs

```python
def test_dialog_interaction(self, main_window):
    """Test dialog interaction."""
    with self.capture_dialog(QFileDialog, return_value="/path/to/file.gguf"):
        # Trigger action that opens dialog
        main_window.open_model_dialog()
    
    # Verify dialog result was processed
    assert main_window.selected_model == "/path/to/file.gguf"
```

## Addon Testing

### Addon Test Harness

The addon test harness provides utilities for testing addon functionality:

```python
import pytest
from tests.addons.addon_test_harness import AddonTestHarness

pytestmark = pytest.mark.addon

def test_addon_lifecycle(addon_test_harness):
    """Test complete addon lifecycle."""
    # Create test addon
    addon_path = addon_test_harness.create_addon("test-addon", "1.0.0")
    
    # Install addon
    addon_id = addon_test_harness.install_addon(addon_path)
    assert addon_id == "test-addon"
    
    # Enable addon
    success = addon_test_harness.enable_addon(addon_id)
    assert success is True
    
    # Test addon functionality
    addon = addon_test_harness.get_addon_instance(addon_id)
    assert addon is not None
    
    # Cleanup
    addon_test_harness.cleanup()
```

### Custom Addon Testing

```python
def test_custom_addon(addon_test_harness):
    """Test custom addon functionality."""
    # Create addon with custom code
    custom_code = '''
from interfaces.i_addon import IAddon

class CustomAddon(IAddon):
    def initialize(self, app_context):
        self.app_context = app_context
        return True
    
    def get_metadata(self):
        return {
            "id": "custom-addon",
            "name": "Custom Addon",
            "version": "1.0.0"
        }
    
    def custom_method(self):
        return "custom_result"
    '''
    
    # Create and install addon
    addon_path = addon_test_harness.create_addon("custom-addon", "1.0.0", custom_code)
    addon_id = addon_test_harness.install_addon(addon_path)
    addon_test_harness.enable_addon(addon_id)
    
    # Test custom functionality
    addon = addon_test_harness.get_addon_instance(addon_id)
    result = addon.custom_method()
    assert result == "custom_result"
```

### Addon Performance Testing

```python
def test_addon_performance(real_addon_manager):
    """Test addon performance."""
    from tests.addons.addon_test_harness import AddonPerformanceBenchmark
    
    benchmark = AddonPerformanceBenchmark(real_addon_manager)
    
    # Benchmark installation
    installation_time = benchmark.benchmark_installation(addon_path)
    assert installation_time < 5.0  # Should install in under 5 seconds
    
    # Benchmark initialization
    init_time = benchmark.benchmark_initialization("test-addon")
    assert init_time < 1.0  # Should initialize in under 1 second
```

## Performance Testing

### Memory Testing

```python
import pytest

pytestmark = pytest.mark.memory

def test_memory_usage(performance_monitor):
    """Test memory usage during operation."""
    # Set baseline
    performance_monitor.start()
    
    # Perform memory-intensive operation
    component = MemoryIntensiveComponent()
    component.load_large_data()
    
    # Measure memory usage
    performance_monitor.stop()
    
    # Verify memory usage is within acceptable limits
    memory_usage = performance_monitor.get_memory_usage()
    assert memory_usage < 100 * 1024 * 1024  # Less than 100MB
```

### Benchmark Testing

```python
import pytest

pytestmark = pytest.mark.performance

def test_processing_speed(benchmark):
    """Benchmark processing speed."""
    component = ProcessingComponent()
    
    # Benchmark the operation
    result = benchmark(component.process_data, "test_data")
    
    # Verify result and performance
    assert result == "processed: test_data"
    assert benchmark.stats.mean < 0.1  # Should complete in under 100ms
```

### Memory Leak Testing

```python
def test_memory_leak():
    """Test for memory leaks."""
    import gc
    import psutil
    
    process = psutil.Process()
    initial_memory = process.memory_info().rss
    
    # Perform operations that might leak memory
    for i in range(100):
        component = LeakyComponent()
        component.do_work()
        del component
        
        if i % 10 == 0:
            gc.collect()
    
    # Check final memory usage
    final_memory = process.memory_info().rss
    memory_growth = final_memory - initial_memory
    
    # Memory growth should be minimal
    assert memory_growth < 10 * 1024 * 1024  # Less than 10MB growth
```

## Test Utilities

### Mock Objects

The testing framework provides comprehensive mock objects:

```python
from tests.utils.mock_objects import MockGGUFModel, MockAddon, MockModelManager

def test_with_mock_model():
    """Test using mock GGUF model."""
    model = MockGGUFModel.create_mock("test-model", "Test Model")
    
    assert model.id == "test-model"
    assert model.name == "Test Model"
    assert model.loaded is False
```

### Test Helpers

```python
from tests.utils.test_helpers import create_mock_gguf_file, create_mock_addon_package

def test_with_mock_files(temp_dir):
    """Test using mock files."""
    # Create mock GGUF file
    model_file = create_mock_gguf_file(str(temp_dir), "test.gguf", 1024)
    assert os.path.exists(model_file)
    
    # Create mock addon package
    addon_dir = create_mock_addon_package(str(temp_dir), "test-addon", "1.0.0")
    assert os.path.exists(os.path.join(addon_dir, "addon.json"))
```

### Event Recording

```python
from tests.utils.test_helpers import EventRecorder

def test_event_recording(real_event_bus):
    """Test event recording functionality."""
    recorder = EventRecorder(real_event_bus)
    
    # Start recording
    recorder.start_recording("test.event")
    
    # Trigger events
    real_event_bus.publish("test.event", "data1")
    real_event_bus.publish("test.event", "data2")
    
    # Check recorded events
    events = recorder.get_events("test.event")
    assert len(events) == 2
    assert events[0][0] == ("data1",)
    assert events[1][0] == ("data2",)
```

## Best Practices

### Test Organization

1. **Group related tests** in classes
2. **Use descriptive test names** that explain what is being tested
3. **Follow the AAA pattern**: Arrange, Act, Assert
4. **Keep tests independent** - each test should be able to run in isolation
5. **Use fixtures** for common setup and teardown

### Test Data Management

```python
# Good: Use fixtures for test data
@pytest.fixture
def sample_data():
    return {
        "input": "test input",
        "expected": "expected output"
    }

def test_processing(sample_data):
    result = process(sample_data["input"])
    assert result == sample_data["expected"]

# Avoid: Hardcoded test data in tests
def test_processing_bad():
    result = process("test input")  # Hardcoded data
    assert result == "expected output"  # Hardcoded expectation
```

### Mocking Guidelines

```python
# Good: Mock external dependencies
def test_with_proper_mocking(mock_external_service):
    component = MyComponent(mock_external_service)
    mock_external_service.get_data.return_value = "test_data"
    
    result = component.process()
    
    assert result == "processed: test_data"
    mock_external_service.get_data.assert_called_once()

# Avoid: Testing implementation details
def test_bad_mocking():
    with patch('my_component.internal_method') as mock_internal:
        component = MyComponent()
        component.process()
        mock_internal.assert_called()  # Testing internal implementation
```

### Error Testing

```python
def test_error_handling():
    """Test that errors are handled properly."""
    component = MyComponent()
    
    # Test with invalid input
    with pytest.raises(ValueError, match="Invalid input"):
        component.process(None)
    
    # Test error recovery
    component.handle_error("test error")
    assert component.error_count == 1
    assert component.last_error == "test error"
```

### Performance Testing Guidelines

1. **Use benchmarks** for performance-critical code
2. **Set realistic thresholds** based on requirements
3. **Test on representative hardware** when possible
4. **Monitor memory usage** for long-running operations
5. **Test with realistic data sizes**

## Continuous Integration

### GitHub Actions Configuration

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10']
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python run_test_suite.py ci
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
      with:
        file: ./reports/coverage.xml
```

### Test Configuration for CI

```python
# pytest.ini for CI
[pytest]
addopts = 
    --strict-markers
    --strict-config
    --cov=app
    --cov=interfaces
    --cov-report=xml:reports/coverage.xml
    --junit-xml=reports/junit.xml
    --maxfail=5
    --tb=short

markers =
    unit: Unit tests
    integration: Integration tests
    ui: UI tests (may require display)
    addon: Addon tests
    slow: Slow tests (may be skipped in CI)
    performance: Performance tests
```

### Running Tests in CI

```bash
# Fast CI tests (exclude slow and UI tests)
python run_tests.py -m "not slow and not ui" --parallel

# Full test suite with coverage
python run_test_suite.py ci

# Memory tests
python run_memory_tests.py
```

## Troubleshooting Tests

### Common Issues

#### Qt Application Issues
```python
# Problem: QApplication not available
# Solution: Use qapp fixture
def test_ui_component(qapp):
    widget = MyWidget()
    assert widget is not None
```

#### Mock Configuration Issues
```python
# Problem: Mock not working as expected
# Solution: Verify mock setup
def test_with_debug_mock():
    mock_service = MagicMock()
    mock_service.get_data.return_value = "test"
    
    # Debug mock calls
    result = mock_service.get_data()
    print(f"Mock called: {mock_service.get_data.called}")
    print(f"Mock call args: {mock_service.get_data.call_args}")
```

#### Test Isolation Issues
```python
# Problem: Tests affecting each other
# Solution: Proper cleanup in fixtures
@pytest.fixture
def isolated_component():
    component = MyComponent()
    yield component
    component.cleanup()  # Ensure cleanup
```

### Debugging Tests

```bash
# Run single test with verbose output
python -m pytest tests/test_specific.py::test_method -v -s

# Run with debugger
python -m pytest tests/test_specific.py::test_method --pdb

# Run with coverage and HTML report
python run_tests.py --html --cov-report=html
```

This testing guide provides comprehensive information for testing the GGUF Loader App effectively. Follow these practices to ensure robust, maintainable tests that provide confidence in the application's quality.