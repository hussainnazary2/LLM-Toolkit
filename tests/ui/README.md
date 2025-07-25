# UI Testing Framework

This directory contains the UI testing framework for the GGUF Loader App.

## Overview

The UI testing framework is built on top of pytest and pytest-qt, and provides utilities and fixtures for testing the application's UI components.

## Key Components

- `conftest.py`: Contains fixtures for creating UI components for testing
- `ui_test_utils.py`: Contains the `UITestCase` class with helper methods for UI testing
- `test_ui_framework.py`: Contains tests for the UI testing framework itself
- `test_*.py`: Contains tests for specific UI components

## Usage

### Basic UI Test

```python
import pytest
from tests.utils.ui_test_utils import UITestCase

# Mark the test as a UI test
pytestmark = pytest.mark.ui

class TestMyDialog(UITestCase):
    def test_dialog(self, qapp):
        # Create the dialog
        dialog = MyDialog()
        
        # Click a button
        self.click_button(dialog.ok_button)
        
        # Enter text
        self.enter_text(dialog.name_field, "Test Name")
        
        # Check the result
        assert dialog.result() == QDialog.Accepted
```

### Using Fixtures

```python
import pytest
from tests.utils.ui_test_utils import UITestCase

# Mark the test as a UI test
pytestmark = pytest.mark.ui

class TestMainWindow(UITestCase):
    def test_main_window(self, main_window, mock_event_bus):
        # The main_window fixture creates a MainWindow instance
        
        # Test the window
        assert main_window.isVisible()
        
        # Simulate an event
        mock_event_bus.publish("model.loaded", "test-model")
        
        # Check the result
        assert main_window.model_info_view.isVisible()
```

### Taking Screenshots on Failure

```python
import pytest
from tests.utils.ui_test_utils import UITestCase

# Mark the test as a UI test and use the screenshot_on_failure fixture
pytestmark = [pytest.mark.ui, pytest.mark.usefixtures("screenshot_on_failure")]

class TestComplexUI(UITestCase):
    def test_complex_interaction(self, main_window):
        # If this test fails, a screenshot will be taken automatically
        # and saved to the screenshots directory
        ...
```

## Available Fixtures

- `qapp`: A QApplication instance for UI testing
- `main_window`: A MainWindow instance
- `model_info_view`: A ModelInfoView instance
- `file_dialog`: A FileDialog instance
- `preferences_dialog`: A PreferencesDialog instance
- `error_dialog`: An ErrorDialog instance
- `addon_management_view`: An AddonManagementView instance
- `addon_installation_dialog`: An AddonInstallationDialog instance
- `addon_configuration_dialog`: An AddonConfigurationDialog instance
- `screenshot_on_failure`: Takes a screenshot when a test fails

## UITestCase Methods

The `UITestCase` class provides the following methods:

- `process_events()`: Process pending Qt events
- `wait(ms)`: Wait for the specified number of milliseconds
- `click_button(button)`: Click a button
- `click_item(widget, point=None)`: Click an item in a widget
- `double_click_item(widget, point=None)`: Double-click an item in a widget
- `enter_text(widget, text)`: Enter text in a widget
- `select_combo_item(combo_box, index)`: Select an item in a combo box
- `select_list_item(list_widget, index)`: Select an item in a list widget
- `check_checkbox(checkbox, checked=True)`: Check or uncheck a checkbox
- `resize_widget(widget, width, height)`: Resize a widget
- `wait_for_window(window_class)`: Wait for a window to appear
- `wait_for_signal(signal, timeout=1000)`: Wait for a signal to be emitted
- `capture_dialog(dialog_class, return_value=None)`: Capture a dialog and return a predefined value
- `capture_message_box(return_value=None)`: Capture a message box and return a predefined value

## Running UI Tests

To run the UI tests, use the `run_tests.py` script with the `-m ui` option:

```bash
python run_tests.py -m ui
```

You can also run specific UI test files:

```bash
python run_tests.py tests/ui/test_main_window.py
```

Or specific test methods:

```bash
python run_tests.py tests/ui/test_main_window.py::TestMainWindow::test_main_window_creation
```