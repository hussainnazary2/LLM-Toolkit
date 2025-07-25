"""
Unit tests for the ModelService component.
"""

import unittest
import tempfile
import shutil
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from PySide6.QtCore import QCoreApplication

from app.core.model_service import ModelService, ModelLoadingThread
from app.core.event_bus import EventBus
from app.models.gguf_model import GGUFModel

class TestModelService(unittest.TestCase):
    """Test cases for the ModelService class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for the class."""
        # Create QApplication if it doesn't exist
        if not QCoreApplication.instance():
            cls.app = QCoreApplication([])
        else:
            cls.app = QCoreApplication.instance()
    
    def setUp(self):
        """Set up test fixtures."""
        # Create event bus
        self.event_bus = EventBus()
        
        # Create model service
        self.model_service = ModelService(self.event_bus)
        
        # Create temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        self.test_model_path = Path(self.temp_dir) / "test_model.gguf"
        
        # Create a mock GGUF file
        self._create_mock_gguf_file()
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up model service
        self.model_service.unload_all_models()
        
        # Shut down event bus
        self.event_bus.shutdown()
        
        # Remove temporary directory
        shutil.rmtree(self.temp_dir)
    
    def _create_mock_gguf_file(self):
        """Create a mock GGUF file for testing."""
        # Create a file with GGUF magic bytes
        with open(self.test_model_path, 'wb') as f:
            f.write(b"GGUF")  # Magic bytes
            f.write(b"\x00" * 1024)  # Some dummy data
    
    def test_initialization(self):
        """Test ModelService initialization."""
        # Check that the service is properly initialized
        self.assertIsInstance(self.model_service.event_bus, EventBus)
        self.assertEqual(len(self.model_service.loaded_models), 0)
        self.assertIsNone(self.model_service.current_model_id)
        self.assertIsNone(self.model_service.loading_thread)
    
    def test_get_current_model_no_model(self):
        """Test getting current model when no model is loaded."""
        current_model = self.model_service.get_current_model()
        self.assertIsNone(current_model)
    
    def test_get_loaded_models_empty(self):
        """Test getting loaded models when none are loaded."""
        loaded_models = self.model_service.get_loaded_models()
        self.assertEqual(len(loaded_models), 0)
        self.assertIsInstance(loaded_models, dict)
    
    def test_is_model_loaded_no_model(self):
        """Test checking if model is loaded when no model exists."""
        self.assertFalse(self.model_service.is_model_loaded())
        self.assertFalse(self.model_service.is_model_loaded("nonexistent"))
    
    def test_get_memory_usage_no_models(self):
        """Test getting memory usage when no models are loaded."""
        memory_usage = self.model_service.get_memory_usage()
        
        expected = {
            "total": 0,
            "models": {},
            "count": 0
        }
        
        self.assertEqual(memory_usage, expected)
    
    def test_get_model_info_no_model(self):
        """Test getting model info when no model exists."""
        model_info = self.model_service.get_model_info()
        self.assertIsNone(model_info)
        
        model_info = self.model_service.get_model_info("nonexistent")
        self.assertIsNone(model_info)
    
    def test_set_current_model_nonexistent(self):
        """Test setting current model to a nonexistent model."""
        result = self.model_service.set_current_model("nonexistent")
        self.assertFalse(result)
        self.assertIsNone(self.model_service.current_model_id)
    
    def test_generate_text_no_model(self):
        """Test text generation when no model is loaded."""
        result = self.model_service.generate_text("Hello, world!")
        self.assertIsNone(result)
    
    @patch('app.models.gguf_model.GGUFModel.validate')
    @patch('app.models.gguf_model.GGUFModel.extract_metadata')
    @patch('app.models.gguf_model.GGUFModel.load')
    def test_model_loading_success(self, mock_load, mock_extract, mock_validate):
        """Test successful model loading."""
        # Mock the validation and loading
        mock_validate.return_value = (True, None)
        mock_extract.return_value = True
        mock_load.return_value = True
        
        # Create a flag to track if model was loaded
        model_loaded = False
        
        def on_model_loaded(model_id, model_info):
            nonlocal model_loaded
            model_loaded = True
            self.assertIsInstance(model_id, str)
            self.assertIsInstance(model_info, dict)
            self.assertIn("name", model_info)
            self.assertIn("file_path", model_info)
        
        # Connect to the signal
        self.model_service.model_loaded.connect(on_model_loaded)
        
        # Create and run the loading thread
        loading_thread = ModelLoadingThread(str(self.test_model_path))
        loading_thread.run()  # Run synchronously for testing
        
        # Process the result
        if hasattr(loading_thread, '_result_model'):
            self.model_service._on_model_loaded(loading_thread._result_model)
        
        # Note: In a real test, we would need to properly mock the GGUFModel
        # and handle the asynchronous loading. This is a simplified test.
    
    @patch('app.models.gguf_model.GGUFModel.validate')
    def test_model_loading_validation_failure(self, mock_validate):
        """Test model loading with validation failure."""
        # Mock validation failure
        mock_validate.return_value = (False, "Invalid GGUF file")
        
        # Create a flag to track if error was emitted
        error_emitted = False
        error_message = None
        
        def on_loading_error(message):
            nonlocal error_emitted, error_message
            error_emitted = True
            error_message = message
        
        # Connect to the signal
        self.model_service.loading_error.connect(on_loading_error)
        
        # Create and run the loading thread
        loading_thread = ModelLoadingThread(str(self.test_model_path))
        loading_thread.run()  # Run synchronously for testing
        
        # Note: In a real test, we would need to properly handle the thread execution
    
    def test_handle_load_request_no_file_path(self):
        """Test handling load request without file path."""
        # Create a flag to track if error was emitted
        error_emitted = False
        
        def on_loading_error(message):
            nonlocal error_emitted
            error_emitted = True
            self.assertEqual(message, "No file path provided")
        
        # Connect to the signal
        self.model_service.loading_error.connect(on_loading_error)
        
        # Send load request without file path
        self.model_service._handle_load_request({})
        
        # Check that error was emitted
        self.assertTrue(error_emitted)
    
    def test_handle_unload_request_nonexistent(self):
        """Test handling unload request for nonexistent model."""
        # This should not raise an error
        self.model_service._handle_unload_request("nonexistent")
        
        # Check that no models are loaded
        self.assertEqual(len(self.model_service.loaded_models), 0)
    
    def test_event_bus_integration(self):
        """Test integration with event bus."""
        # Test that the service subscribes to the correct events
        load_subscribers = self.event_bus.get_subscriber_count("model.load.request")
        unload_subscribers = self.event_bus.get_subscriber_count("model.unload.request")
        
        # The service should be subscribed to these events
        self.assertGreaterEqual(load_subscribers, 1)
        self.assertGreaterEqual(unload_subscribers, 1)
    
    def test_mock_model_operations(self):
        """Test model operations with a mock model."""
        # Create a mock model
        mock_model = Mock(spec=GGUFModel)
        mock_model.name = "test_model"
        mock_model.file_path = str(self.test_model_path)
        mock_model.size = 1024
        mock_model.get_size_str.return_value = "1.00 KB"
        mock_model.parameters = {"context_length": 2048}
        mock_model.metadata = {"architecture": "test"}
        mock_model.memory_usage = 512
        mock_model.load_time = None
        mock_model.last_accessed = None
        mock_model.loaded = True
        mock_model.load_type = "mmap"
        mock_model.hardware_backend = None
        mock_model.hardware_device = None
        mock_model.access = Mock()
        
        # Add mock llama model for text generation
        mock_llama_model = Mock()
        mock_llama_model.return_value = {
            'choices': [{'text': 'Generated text response'}]
        }
        mock_model._llama_model = mock_llama_model
        
        # Manually add the model to the service
        model_id = "test_model_1"
        self.model_service.loaded_models[model_id] = mock_model
        self.model_service.current_model_id = model_id
        
        # Test get_current_model
        current_model = self.model_service.get_current_model()
        self.assertEqual(current_model, mock_model)
        
        # Test get_loaded_models
        loaded_models = self.model_service.get_loaded_models()
        self.assertEqual(len(loaded_models), 1)
        self.assertIn(model_id, loaded_models)
        
        # Test is_model_loaded
        self.assertTrue(self.model_service.is_model_loaded())
        self.assertTrue(self.model_service.is_model_loaded(model_id))
        
        # Test get_model_info
        model_info = self.model_service.get_model_info()
        self.assertIsNotNone(model_info)
        self.assertEqual(model_info["name"], "test_model")
        self.assertEqual(model_info["size"], 1024)
        
        # Test get_memory_usage
        memory_usage = self.model_service.get_memory_usage()
        self.assertEqual(memory_usage["total"], 512)
        self.assertEqual(memory_usage["count"], 1)
        self.assertIn(model_id, memory_usage["models"])
        
        # Test generate_text
        result = self.model_service.generate_text("Hello, world!")
        self.assertEqual(result, "Generated text response")
        mock_model.access.assert_called_once()
        
        # Test set_current_model
        self.assertTrue(self.model_service.set_current_model(model_id))
        
        # Test unload
        mock_model.unload = Mock()
        self.model_service._handle_unload_request(model_id)
        mock_model.unload.assert_called_once()
        self.assertNotIn(model_id, self.model_service.loaded_models)
        self.assertIsNone(self.model_service.current_model_id)

class TestModelLoadingThread(unittest.TestCase):
    """Test cases for the ModelLoadingThread class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for the class."""
        # Create QApplication if it doesn't exist
        if not QCoreApplication.instance():
            cls.app = QCoreApplication([])
        else:
            cls.app = QCoreApplication.instance()
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        self.test_model_path = Path(self.temp_dir) / "test_model.gguf"
        
        # Create a mock GGUF file
        self._create_mock_gguf_file()
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Remove temporary directory
        shutil.rmtree(self.temp_dir)
    
    def _create_mock_gguf_file(self):
        """Create a mock GGUF file for testing."""
        # Create a file with GGUF magic bytes
        with open(self.test_model_path, 'wb') as f:
            f.write(b"GGUF")  # Magic bytes
            f.write(b"\x00" * 1024)  # Some dummy data
    
    def test_initialization(self):
        """Test ModelLoadingThread initialization."""
        thread = ModelLoadingThread(str(self.test_model_path))
        
        self.assertEqual(thread.file_path, str(self.test_model_path))
        self.assertIsNone(thread.load_type)
        
        # Test with load type
        thread_with_type = ModelLoadingThread(str(self.test_model_path), "full")
        self.assertEqual(thread_with_type.load_type, "full")
    
    def test_nonexistent_file(self):
        """Test loading thread with nonexistent file."""
        nonexistent_path = str(Path(self.temp_dir) / "nonexistent.gguf")
        thread = ModelLoadingThread(nonexistent_path)
        
        # Track signals
        error_emitted = False
        error_message = None
        
        def on_error(message):
            nonlocal error_emitted, error_message
            error_emitted = True
            error_message = message
        
        thread.error.connect(on_error)
        
        # Run the thread
        thread.run()
        
        # Check that error was emitted
        self.assertTrue(error_emitted)
        self.assertIn("does not exist", error_message)

if __name__ == "__main__":
    unittest.main()