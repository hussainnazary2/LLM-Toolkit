"""
Tests for the MainWindow class.
"""

import os
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog

from app.ui.main_window import MainWindow
from app.core.event_bus import EventBus
from tests.utils.ui_test_utils import UITestCase
from tests.utils.test_helpers import create_mock_gguf_file

# Mark all tests in this module as UI tests
pytestmark = pytest.mark.ui

class TestMainWindow(UITestCase):
    """Test the MainWindow class."""
    
    def test_main_window_creation(self, main_window):
        """Test creating a MainWindow."""
        # Check that the window has the correct title
        assert "GGUF Loader" in main_window.windowTitle()
        
        # Check that the window is visible
        assert main_window.isVisible()
        
        # Check that the main components are created
        assert main_window.model_info_view is not None
        assert main_window.status_bar is not None
        assert main_window.menu_bar is not None
    
    def test_file_menu_actions(self, main_window, mock_event_bus, temp_dir):
        """Test the file menu actions."""
        # Create a mock GGUF file
        gguf_file = create_mock_gguf_file(temp_dir, "test_model.gguf")
        
        # Mock the QFileDialog.getOpenFileName method
        with patch('PySide6.QtWidgets.QFileDialog.getOpenFileName', return_value=(gguf_file, "GGUF Files (*.gguf)")):
            # Trigger the open file action
            main_window.file_menu.actions()[0].trigger()  # Assuming the first action is "Open"
            
            # Check that the event bus was called to load the model
            mock_event_bus.publish.assert_any_call("model.load_requested", gguf_file)
    
    def test_view_menu_actions(self, main_window):
        """Test the view menu actions."""
        # Get the view menu actions
        view_actions = main_window.view_menu.actions()
        
        # Find the toggle model info action
        toggle_model_info_action = None
        for action in view_actions:
            if "Model Info" in action.text():
                toggle_model_info_action = action
                break
        
        assert toggle_model_info_action is not None
        
        # Check the initial state
        initial_visible = main_window.model_info_view.isVisible()
        
        # Trigger the action
        toggle_model_info_action.trigger()
        
        # Check that the visibility was toggled
        assert main_window.model_info_view.isVisible() != initial_visible
        
        # Trigger the action again to restore the original state
        toggle_model_info_action.trigger()
        
        # Check that the visibility was restored
        assert main_window.model_info_view.isVisible() == initial_visible
    
    def test_tools_menu_actions(self, main_window):
        """Test the tools menu actions."""
        # Get the tools menu actions
        tools_actions = main_window.tools_menu.actions()
        
        # Find the preferences action
        preferences_action = None
        for action in tools_actions:
            if "Preferences" in action.text():
                preferences_action = action
                break
        
        assert preferences_action is not None
        
        # Mock the PreferencesDialog
        with patch('app.ui.main_window.PreferencesDialog') as mock_dialog_class:
            # Configure the mock dialog
            mock_dialog = MagicMock()
            mock_dialog_class.return_value = mock_dialog
            
            # Trigger the action
            preferences_action.trigger()
            
            # Check that the dialog was created and shown
            mock_dialog_class.assert_called_once()
            mock_dialog.exec.assert_called_once()
    
    def test_addons_menu_actions(self, main_window):
        """Test the addons menu actions."""
        # Get the addons menu actions
        addons_actions = main_window.addons_menu.actions()
        
        # Find the manage addons action
        manage_addons_action = None
        for action in addons_actions:
            if "Manage Addons" in action.text():
                manage_addons_action = action
                break
        
        assert manage_addons_action is not None
        
        # Mock the AddonManagementDialog
        with patch('app.ui.main_window.AddonManagementDialog') as mock_dialog_class:
            # Configure the mock dialog
            mock_dialog = MagicMock()
            mock_dialog_class.return_value = mock_dialog
            
            # Trigger the action
            manage_addons_action.trigger()
            
            # Check that the dialog was created and shown
            mock_dialog_class.assert_called_once()
            mock_dialog.exec.assert_called_once()
    
    def test_help_menu_actions(self, main_window):
        """Test the help menu actions."""
        # Get the help menu actions
        help_actions = main_window.help_menu.actions()
        
        # Find the about action
        about_action = None
        for action in help_actions:
            if "About" in action.text():
                about_action = action
                break
        
        assert about_action is not None
        
        # Mock the QMessageBox.about method
        with patch('PySide6.QtWidgets.QMessageBox.about') as mock_about:
            # Trigger the action
            about_action.trigger()
            
            # Check that the about dialog was shown
            mock_about.assert_called_once()
    
    def test_status_bar_updates(self, main_window, mock_event_bus):
        """Test status bar updates."""
        # Get the status bar
        status_bar = main_window.status_bar
        
        # Check the initial status
        assert status_bar.currentMessage() == "Ready"
        
        # Simulate a status update event
        mock_event_bus.publish("status.update", "Loading model...")
        
        # Check that the status was updated
        assert status_bar.currentMessage() == "Loading model..."
    
    def test_drag_drop_handling(self, main_window, mock_event_bus, temp_dir):
        """Test drag and drop handling."""
        # Create a mock GGUF file
        gguf_file = create_mock_gguf_file(temp_dir, "test_model.gguf")
        
        # Mock the drag_drop_handler
        main_window.drag_drop_handler.handle_drop.return_value = True
        
        # Simulate a drag and drop event
        main_window.handle_drop_event([gguf_file])
        
        # Check that the drag_drop_handler was called
        main_window.drag_drop_handler.handle_drop.assert_called_once_with([gguf_file])
    
    def test_window_resize(self, main_window, mock_config_manager):
        """Test window resize handling."""
        # Resize the window
        self.resize_widget(main_window, 1000, 800)
        
        # Simulate the window close event to trigger saving the size
        main_window.closeEvent(MagicMock())
        
        # Check that the config manager was called to save the window size
        mock_config_manager.set_value.assert_any_call("window_size", (1000, 800))
    
    @pytest.mark.parametrize("model_loaded", [True, False])
    def test_model_loaded_state(self, main_window, mock_event_bus, model_loaded):
        """Test the UI state when a model is loaded or unloaded."""
        # Get the actions that should be enabled only when a model is loaded
        model_dependent_actions = []
        for menu in [main_window.file_menu, main_window.tools_menu]:
            for action in menu.actions():
                if hasattr(action, 'requires_model') and action.requires_model:
                    model_dependent_actions.append(action)
        
        # Ensure we found some actions
        assert len(model_dependent_actions) > 0
        
        # Simulate a model loaded or unloaded event
        if model_loaded:
            mock_event_bus.publish("model.loaded", "test-model")
        else:
            mock_event_bus.publish("model.unloaded", "test-model")
        
        # Check that the actions are enabled or disabled appropriately
        for action in model_dependent_actions:
            assert action.isEnabled() == model_loaded