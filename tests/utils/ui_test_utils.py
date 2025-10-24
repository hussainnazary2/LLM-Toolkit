"""
Utilities for UI testing.
"""

import os
import sys
import time
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

from PySide6.QtCore import Qt, QTimer, QPoint, QSize
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
from PySide6.QtTest import QTest

class UITestCase:
    """Base class for UI test cases."""
    
    @staticmethod
    def process_events():
        """Process pending Qt events."""
        QApplication.processEvents()
    
    @staticmethod
    def wait(ms):
        """
        Wait for the specified number of milliseconds.
        
        Args:
            ms: Time to wait in milliseconds
        """
        start = time.time()
        end = start + (ms / 1000.0)
        while time.time() < end:
            QApplication.processEvents()
            time.sleep(0.01)
    
    @staticmethod
    def click_button(button):
        """
        Click a button.
        
        Args:
            button: The button to click
        """
        QTest.mouseClick(button, Qt.LeftButton)
    
    @staticmethod
    def click_item(widget, point=None):
        """
        Click an item in a widget.
        
        Args:
            widget: The widget to click
            point: The point to click (default: center)
        """
        if point is None:
            point = QPoint(widget.width() // 2, widget.height() // 2)
        QTest.mouseClick(widget, Qt.LeftButton, pos=point)
    
    @staticmethod
    def double_click_item(widget, point=None):
        """
        Double-click an item in a widget.
        
        Args:
            widget: The widget to click
            point: The point to click (default: center)
        """
        if point is None:
            point = QPoint(widget.width() // 2, widget.height() // 2)
        QTest.mouseDClick(widget, Qt.LeftButton, pos=point)
    
    @staticmethod
    def enter_text(widget, text):
        """
        Enter text in a widget.
        
        Args:
            widget: The widget to enter text into
            text: The text to enter
        """
        widget.clear()
        QTest.keyClicks(widget, text)
    
    @staticmethod
    def select_combo_item(combo_box, index):
        """
        Select an item in a combo box.
        
        Args:
            combo_box: The combo box
            index: The index to select
        """
        combo_box.setCurrentIndex(index)
        UITestCase.process_events()
    
    @staticmethod
    def select_list_item(list_widget, index):
        """
        Select an item in a list widget.
        
        Args:
            list_widget: The list widget
            index: The index to select
        """
        list_widget.setCurrentRow(index)
        UITestCase.process_events()
    
    @staticmethod
    def check_checkbox(checkbox, checked=True):
        """
        Check or uncheck a checkbox.
        
        Args:
            checkbox: The checkbox
            checked: Whether to check or uncheck
        """
        if checkbox.isChecked() != checked:
            UITestCase.click_button(checkbox)
    
    @staticmethod
    def resize_widget(widget, width, height):
        """
        Resize a widget.
        
        Args:
            widget: The widget to resize
            width: The new width
            height: The new height
        """
        widget.resize(QSize(width, height))
        UITestCase.process_events()
    
    @staticmethod
    @contextmanager
    def wait_for_window(window_class):
        """
        Wait for a window to appear.
        
        Args:
            window_class: The window class to wait for
            
        Yields:
            The found window
        """
        found_window = None
        
        # Find the window
        for _ in range(50):  # Try for up to 5 seconds (50 * 0.1s)
            for window in QApplication.topLevelWidgets():
                if isinstance(window, window_class):
                    found_window = window
                    break
            
            if found_window is not None:
                break
            
            UITestCase.wait(100)
        
        if found_window is None:
            raise TimeoutError(f"Window of class {window_class.__name__} did not appear")
        
        yield found_window
    
    @staticmethod
    @contextmanager
    def wait_for_signal(signal, timeout=1000):
        """
        Wait for a signal to be emitted.
        
        Args:
            signal: The signal to wait for
            timeout: Timeout in milliseconds
            
        Yields:
            A list that will contain the signal arguments when emitted
        """
        result = []
        
        def slot(*args):
            result.extend(args)
        
        connection = signal.connect(slot)
        try:
            yield result
            
            # Start a timer to handle the timeout
            timer = QTimer()
            timer.setSingleShot(True)
            timer.start(timeout)
            
            # Wait for either the signal or the timeout
            while not result and timer.isActive():
                QApplication.processEvents()
                time.sleep(0.01)
        finally:
            signal.disconnect(connection)
    
    @staticmethod
    def capture_dialog(dialog_class, return_value=None):
        """
        Capture a dialog and return a predefined value.
        
        Args:
            dialog_class: The dialog class to capture
            return_value: The value to return from the dialog
            
        Returns:
            A context manager that captures the dialog
        """
        mock_dialog = MagicMock()
        if return_value is not None:
            mock_dialog.exec.return_value = return_value
        
        return patch(dialog_class, return_value=mock_dialog)
    
    @staticmethod
    def capture_message_box(return_value=None):
        """
        Capture a message box and return a predefined value.
        
        Args:
            return_value: The value to return from the message box
            
        Returns:
            A context manager that captures the message box
        """
        return patch('PySide6.QtWidgets.QMessageBox.exec', return_value=return_value)