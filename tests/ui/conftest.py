"""
Pytest fixtures for UI testing.
"""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import MagicMock

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt

# Import application components
from app.ui.main_window import MainWindow
from app.ui.model_info_view import ModelInfoView
from app.ui.file_dialog import GGUFFileDialog
from app.ui.preferences_dialog import PreferencesDialog
from app.ui.error_dialog import ErrorDetailsDialog
from app.ui.addon_management_view import AddonManagementView
from app.ui.addon_installation_dialog import AddonInstallationDialog
from app.ui.addon_configuration_dialog import AddonConfigurationDialog

# Import test utilities
from tests.utils.mock_objects import (
    MockModelManager,
    MockAddonManager,
    MockGGUFModel,
    MockAppConfig
)

@pytest.fixture
def main_window(qapp, mock_event_bus, mock_config_manager):
    """Create a MainWindow instance for testing."""
    # Create mock components
    model_manager = MockModelManager.create_mock()
    addon_manager = MockAddonManager.create_mock()
    
    # Create the main window
    window = MainWindow(
        event_bus=mock_event_bus,
        config_manager=mock_config_manager,
        model_manager=model_manager,
        addon_manager=addon_manager
    )
    
    # Show the window (but don't actually display it)
    window.show()
    QApplication.processEvents()
    
    yield window
    
    # Clean up
    window.close()
    QApplication.processEvents()

@pytest.fixture
def model_info_view(qapp, mock_event_bus):
    """Create a ModelInfoView instance for testing."""
    # Create mock model
    model = MockGGUFModel.create_mock("test-model", "Test Model")
    
    # Create the view
    view = ModelInfoView(mock_event_bus)
    
    # Set the model
    view.set_model(model)
    
    # Show the view
    view.show()
    QApplication.processEvents()
    
    yield view
    
    # Clean up
    view.close()
    QApplication.processEvents()

@pytest.fixture
def file_dialog(qapp, mock_config_manager):
    """Create a GGUFFileDialog instance for testing."""
    # Create the dialog
    dialog = GGUFFileDialog()
    
    yield dialog
    
    # Clean up
    dialog.close()
    QApplication.processEvents()

@pytest.fixture
def preferences_dialog(qapp, mock_config_manager, mock_event_bus):
    """Create a PreferencesDialog instance for testing."""
    # Create the dialog
    dialog = PreferencesDialog(mock_config_manager, mock_event_bus)
    
    yield dialog
    
    # Clean up
    dialog.close()
    QApplication.processEvents()

@pytest.fixture
def error_dialog(qapp):
    """Create an ErrorDetailsDialog instance for testing."""
    # Create the dialog
    test_error = Exception("This is a test error message.")
    dialog = ErrorDetailsDialog(test_error, "test", "Test Error")
    
    yield dialog
    
    # Clean up
    dialog.close()
    QApplication.processEvents()

@pytest.fixture
def addon_management_view(qapp, mock_addon_manager):
    """Create an AddonManagementView instance for testing."""
    # Create the view
    view = AddonManagementView(mock_addon_manager)
    
    # Show the view
    view.show()
    QApplication.processEvents()
    
    yield view
    
    # Clean up
    view.close()
    QApplication.processEvents()

@pytest.fixture
def addon_installation_dialog(qapp, mock_addon_manager, mock_event_bus):
    """Create an AddonInstallationDialog instance for testing."""
    # Create the dialog
    dialog = AddonInstallationDialog(mock_addon_manager, mock_event_bus)
    
    yield dialog
    
    # Clean up
    dialog.close()
    QApplication.processEvents()

@pytest.fixture
def addon_configuration_dialog(qapp, mock_addon_manager, mock_event_bus):
    """Create an AddonConfigurationDialog instance for testing."""
    # Create the dialog
    dialog = AddonConfigurationDialog(mock_addon_manager, "addon1", mock_event_bus)
    
    yield dialog
    
    # Clean up
    dialog.close()
    QApplication.processEvents()

@pytest.fixture
def screenshot_on_failure(request, qapp):
    """
    Take a screenshot when a test fails.
    
    Usage:
        @pytest.mark.usefixtures("screenshot_on_failure")
        def test_something(qapp):
            ...
    """
    yield
    
    # Check if the test failed
    if request.node.rep_call.failed:
        # Get the test name
        test_name = request.node.name
        
        # Create screenshots directory if it doesn't exist
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)
        
        # Take a screenshot of all top-level windows
        for i, window in enumerate(QApplication.topLevelWidgets()):
            if isinstance(window, QMainWindow) and window.isVisible():
                # Create a unique filename
                filename = f"screenshots/{test_name}_{i}.png"
                
                # Take the screenshot
                pixmap = window.grab()
                pixmap.save(filename)
                
                print(f"Screenshot saved to {filename}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Store the test result for the screenshot_on_failure fixture.
    """
    # Execute the hook
    outcome = yield
    
    # Get the result
    rep = outcome.get_result()
    
    # Set the result attribute on the test node
    setattr(item, f"rep_{rep.when}", rep)