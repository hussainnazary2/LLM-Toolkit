# Test Utilities

This directory contains utilities and helpers for testing the GGUF Loader App.

## Overview

The test utilities are organized into the following modules:

- `test_helpers.py`: General helper functions for testing
- `mock_objects.py`: Mock implementations of application components
- `ui_test_utils.py`: Utilities for UI testing

## Usage

### Test Helpers

The `test_helpers.py` module provides functions for creating test data and utilities for testing:

```python
from tests.utils.test_helpers import create_mock_gguf_file, create_mock_addon_package, EventRecorder

# Create a mock GGUF file for testing
file_path = create_mock_gguf_file("/tmp", "test.gguf", 1024)

# Create a mock addon package for testing
addon_dir = create_mock_addon_package("/tmp", "test-addon", "1.0.0")

# Record events from the EventBus
event_bus = get_event_bus()
recorder = EventRecorder(event_bus)
recorder.start_recording("test.event")
# ... trigger events ...
events = recorder.get_events("test.event")
```

### Mock Objects

The `mock_objects.py` module provides mock implementations of application components:

```python
from tests.utils.mock_objects import MockGGUFModel, MockAddon, MockModelManager, MockAddonManager

# Create a mock GGUF model
model = MockGGUFModel.create_mock("test-model", "Test Model")

# Create a mock addon
addon, metadata, state = MockAddon.create_mock("test-addon", "Test Addon", "1.0.0", True)

# Create a mock model manager
model_manager = MockModelManager.create_mock()

# Create a mock addon manager
addon_manager = MockAddonManager.create_mock()
```

### UI Test Utilities

The `ui_test_utils.py` module provides utilities for UI testing:

```python
from tests.utils.ui_test_utils import UITestCase

class TestMyDialog(UITestCase):
    def test_dialog(self, qapp):
        # Create the dialog
        dialog = MyDialog()
        
        # Click a button
        self.click_button(dialog.ok_button)
        
        # Enter text
        self.enter_text(dialog.name_field, "Test Name")
        
        # Select an item
        self.select_combo_item(dialog.type_combo, 1)
        
        # Wait for a signal
        with self.wait_for_signal(dialog.finished):
            self.click_button(dialog.apply_button)
```

## Fixtures

Common fixtures are defined in `conftest.py` at the root of the tests directory:

- `qapp`: A QApplication instance for UI testing
- `temp_dir`: A temporary directory for test files
- `mock_event_bus`: A mock EventBus
- `mock_config_manager`: A mock ConfigManager

## Running Tests

To run the tests, use the `run_tests.py` script:

```bash
python run_tests.py
```

You can also run specific tests or test modules:

```bash
python run_tests.py tests/utils/test_mock_objects.py
python run_tests.py tests/utils/test_mock_objects.py::test_mock_gguf_model
```

To run tests with specific markers:

```bash
python run_tests.py -m unit
python run_tests.py -m ui
```