"""
Unit tests for backend manager functionality.

Tests the BackendManager class including:
- Backend lifecycle management
- Automatic fallback logic
- Backend selection and switching
- Configuration management
- Performance monitoring integration
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import time
from pathlib import Path

from core.backend_manager import BackendManager, BackendStatus
from core.model_backends import (
    BackendConfig, BackendType, HardwareInfo, LoadingResult, 
    GenerationConfig, ModelLoadingError
)
from core.hardware_detector import HardwareDetector


class TestBackendStatus:
    """Test BackendStatus data structure."""
    
    def test_backend_status_creation(self):
        """Test creating backend status."""
        status = BackendStatus(
            name="ctransformers",
            available=True,
            error_message=None,
            last_checked=time.time(),
            load_attempts=5,
            success_count=4,
            failure_count=1,
            average_load_time=2.5
        )
        
        assert status.name == "ctransformers"
        assert status.available is True
        assert status.error_message is None
        assert status.load_attempts == 5
        assert status.success_count == 4
        assert status.failure_count == 1
        assert status.average_load_time == 2.5
    
    def test_backend_status_defaults(self):
        """Test backend status with default values."""
        status = BackendStatus(
            name="test_backend",
            available=False,
            error_message="Test error",
            last_checked=time.time()
        )
        
        assert status.load_attempts == 0
        assert status.success_count == 0
        assert status.failure_count == 0
        assert status.average_load_time == 0.0


class TestBackendManager:
    """Test BackendManager functionality."""
    
    def setup_method(self):
        """Set up test backend manager."""
        # Mock hardware detector
        self.mock_hardware_detector = Mock(spec=HardwareDetector)
        self.mock_hardware_detector.get_hardware_info.return_value = HardwareInfo(
            gpu_count=1,
            total_vram=8192,
            cpu_cores=8,
            total_ram=16384,
            recommended_backend="ctransformers"
        )
        self.mock_hardware_detector.get_optimal_settings.return_value = {
            'gpu_enabled': True,
            'gpu_layers': -1,
            'context_size': 4096,
            'batch_size': 512,
            'threads': 8
        }
        
        # Create backend manager with mocked hardware detector
        with patch('core.backend_manager.monitoring_manager'), \
             patch.object(BackendManager, '_ensure_backends_registered'), \
             patch.object(BackendManager, '_detect_available_backends'):
            
            self.manager = BackendManager(self.mock_hardware_detector)
            
            # Set up mock backend status
            self.manager.backend_status = {
                "ctransformers": BackendStatus(
                    name="ctransformers",
                    available=True,
                    error_message=None,
                    last_checked=time.time()
                ),
                "transformers": BackendStatus(
                    name="transformers", 
                    available=True,
                    error_message=None,
                    last_checked=time.time()
                ),
                "llamafile": BackendStatus(
                    name="llamafile",
                    available=False,
                    error_message="Not installed",
                    last_checked=time.time()
                )
            }
    
    def test_initialization(self):
        """Test backend manager initialization."""
        assert self.manager.hardware_detector == self.mock_hardware_detector
        assert isinstance(self.manager.backends, dict)
        assert isinstance(self.manager.backend_status, dict)
        assert isinstance(self.manager.configs, dict)
        assert self.manager.current_backend is None
        assert self.manager.current_model_path is None
        assert isinstance(self.manager.fallback_order, list)
    
    def test_get_available_backends(self):
        """Test getting available backends."""
        available = self.manager.get_available_backends()
        
        assert "ctransformers" in available
        assert "transformers" in available
        assert "llamafile" not in available  # Marked as unavailable
    
    def test_get_backend_status(self):
        """Test getting backend status."""
        status = self.manager.get_backend_status("ctransformers")
        
        assert isinstance(status, BackendStatus)
        assert status.name == "ctransformers"
        assert status.available is True
        
        # Test non-existent backend
        status = self.manager.get_backend_status("nonexistent")
        assert status is None
    
    def test_get_best_backend_auto(self):
        """Test automatic best backend selection."""
        best = self.manager.get_best_backend(model_size_mb=4096)
        
        # Should return the recommended backend from hardware detector
        assert best == "ctransformers"
    
    def test_get_best_backend_gpu_preference(self):
        """Test best backend selection with GPU preference."""
        best = self.manager.get_best_backend(
            model_size_mb=4096, 
            hardware_preference='gpu'
        )
        
        # Should prefer GPU-capable backends
        assert best in ["ctransformers", "transformers"]
    
    def test_get_best_backend_cpu_preference(self):
        """Test best backend selection with CPU preference."""
        best = self.manager.get_best_backend(
            model_size_mb=4096,
            hardware_preference='cpu'
        )
        
        # Should prefer CPU-friendly backends
        assert best in ["ctransformers"]  # llamafile not available in test
    
    def test_get_best_backend_no_available(self):
        """Test best backend selection when no backends available."""
        # Clear available backends
        for status in self.manager.backend_status.values():
            status.available = False
        
        best = self.manager.get_best_backend()
        assert best is None
    
    def test_can_handle_model_size_sufficient_memory(self):
        """Test model size handling with sufficient memory."""
        can_handle = self.manager._can_handle_model_size("ctransformers", 2048)  # 2GB model
        assert can_handle is True
    
    def test_can_handle_model_size_insufficient_memory(self):
        """Test model size handling with insufficient memory."""
        # Mock low memory system
        self.mock_hardware_detector.get_hardware_info.return_value = HardwareInfo(
            total_ram=4096,  # Only 4GB RAM
            total_vram=2048   # Only 2GB VRAM
        )
        
        can_handle = self.manager._can_handle_model_size("ctransformers", 8192)  # 8GB model
        assert can_handle is False
    
    def test_load_model_success(self, mock_model_file):
        """Test successful model loading."""
        # Mock backend instance
        mock_backend = Mock()
        mock_backend.load_model.return_value = LoadingResult(
            success=True,
            backend_used="ctransformers",
            hardware_used="cuda",
            load_time=2.5,
            memory_usage=4096
        )
        
        with patch.object(self.manager, '_get_backend_instance', return_value=mock_backend):
            result = self.manager.load_model(str(mock_model_file))
        
        assert result.success is True
        assert result.backend_used == "ctransformers"
        assert self.manager.current_backend == mock_backend
        assert self.manager.current_model_path == str(mock_model_file)
    
    def test_load_model_nonexistent_file(self):
        """Test model loading with nonexistent file."""
        result = self.manager.load_model("nonexistent.gguf")
        
        assert result.success is False
        assert "does not exist" in result.error_message
        assert self.manager.current_backend is None
    
    def test_load_model_fallback_success(self, mock_model_file):
        """Test model loading with fallback to secondary backend."""
        # Mock first backend failure, second backend success
        mock_backend1 = Mock()
        mock_backend1.load_model.return_value = LoadingResult(
            success=False,
            backend_used="ctransformers",
            hardware_used="none",
            load_time=0.1,
            error_message="GPU out of memory"
        )
        
        mock_backend2 = Mock()
        mock_backend2.load_model.return_value = LoadingResult(
            success=True,
            backend_used="transformers",
            hardware_used="cpu",
            load_time=3.0,
            memory_usage=2048
        )
        
        def mock_get_backend(name):
            if name == "ctransformers":
                return mock_backend1
            elif name == "transformers":
                return mock_backend2
            return Mock()
        
        with patch.object(self.manager, '_get_backend_instance', side_effect=mock_get_backend):
            result = self.manager.load_model(str(mock_model_file))
        
        assert result.success is True
        assert result.backend_used == "transformers"
        assert self.manager.current_backend == mock_backend2
    
    def test_load_model_all_backends_fail(self, mock_model_file):
        """Test model loading when all backends fail."""
        # Mock all backends failing
        mock_backend = Mock()
        mock_backend.load_model.return_value = LoadingResult(
            success=False,
            backend_used="test",
            hardware_used="none",
            load_time=0.1,
            error_message="Backend failed"
        )
        
        with patch.object(self.manager, '_get_backend_instance', return_value=mock_backend):
            result = self.manager.load_model(str(mock_model_file))
        
        assert result.success is False
        assert "All backends failed" in result.error_message
        assert self.manager.current_backend is None
    
    def test_load_model_specific_backend(self, mock_model_file):
        """Test loading model with specific backend."""
        mock_backend = Mock()
        mock_backend.load_model.return_value = LoadingResult(
            success=True,
            backend_used="transformers",
            hardware_used="cpu",
            load_time=2.0,
            memory_usage=3072
        )
        
        with patch.object(self.manager, '_get_backend_instance', return_value=mock_backend):
            result = self.manager.load_model(str(mock_model_file), backend_name="transformers")
        
        assert result.success is True
        assert result.backend_used == "transformers"
        assert self.manager.current_backend == mock_backend
    
    def test_load_model_specific_backend_unavailable(self, mock_model_file):
        """Test loading model with unavailable specific backend."""
        result = self.manager.load_model(str(mock_model_file), backend_name="llamafile")
        
        assert result.success is False
        assert "not available" in result.error_message
    
    def test_generate_text_success(self):
        """Test successful text generation."""
        # Set up loaded backend
        mock_backend = Mock()
        mock_backend.generate_text.return_value = "Generated response"
        mock_backend.config.name = "ctransformers"
        self.manager.current_backend = mock_backend
        self.manager.current_model_path = "test.gguf"
        
        gen_config = GenerationConfig(max_tokens=100)
        
        with patch.object(self.manager.performance_monitor, 'start_operation', return_value="op_id"), \
             patch.object(self.manager.performance_monitor, 'end_operation'):
            
            result = self.manager.generate_text("Hello", gen_config)
        
        assert result == "Generated response"
        mock_backend.generate_text.assert_called_once_with("Hello", gen_config)
    
    def test_generate_text_no_model(self):
        """Test text generation without loaded model."""
        gen_config = GenerationConfig()
        
        with pytest.raises(ModelLoadingError, match="No model is currently loaded"):
            self.manager.generate_text("Hello", gen_config)
    
    def test_unload_model_success(self):
        """Test successful model unloading."""
        # Set up loaded backend
        mock_backend = Mock()
        mock_backend.unload_model.return_value = True
        mock_backend.config.name = "ctransformers"
        self.manager.current_backend = mock_backend
        self.manager.current_model_path = "test.gguf"
        
        with patch.object(self.manager.performance_monitor, 'start_operation', return_value="op_id"), \
             patch.object(self.manager.performance_monitor, 'end_operation'):
            
            success = self.manager.unload_model()
        
        assert success is True
        assert self.manager.current_backend is None
        assert self.manager.current_model_path is None
        mock_backend.unload_model.assert_called_once()
    
    def test_unload_model_no_model(self):
        """Test unloading when no model is loaded."""
        success = self.manager.unload_model()
        assert success is True
    
    def test_switch_backend_success(self, mock_model_file):
        """Test successful backend switching."""
        # Set up current backend
        mock_current_backend = Mock()
        mock_current_backend.unload_model.return_value = True
        self.manager.current_backend = mock_current_backend
        self.manager.current_model_path = str(mock_model_file)
        
        # Mock new backend
        mock_new_backend = Mock()
        mock_new_backend.load_model.return_value = LoadingResult(
            success=True,
            backend_used="transformers",
            hardware_used="cpu",
            load_time=2.0
        )
        
        with patch.object(self.manager, '_get_backend_instance', return_value=mock_new_backend):
            success = self.manager.switch_backend("transformers", reload_model=True)
        
        assert success is True
        assert self.manager.current_backend == mock_new_backend
        mock_current_backend.unload_model.assert_called_once()
        mock_new_backend.load_model.assert_called_once_with(str(mock_model_file), "transformers")
    
    def test_switch_backend_unavailable(self):
        """Test switching to unavailable backend."""
        success = self.manager.switch_backend("llamafile")
        assert success is False
    
    def test_switch_backend_no_reload(self):
        """Test backend switching without model reload."""
        # Set up current backend
        mock_current_backend = Mock()
        mock_current_backend.unload_model.return_value = True
        self.manager.current_backend = mock_current_backend
        
        success = self.manager.switch_backend("transformers", reload_model=False)
        assert success is True
        mock_current_backend.unload_model.assert_called_once()
    
    def test_get_current_backend_info_loaded(self):
        """Test getting current backend info when model is loaded."""
        mock_backend = Mock()
        mock_backend.get_model_info.return_value = {
            "backend": "ctransformers",
            "model_path": "test.gguf",
            "load_time": 2.5
        }
        self.manager.current_backend = mock_backend
        
        info = self.manager.get_current_backend_info()
        
        assert info is not None
        assert info["backend"] == "ctransformers"
        assert info["model_path"] == "test.gguf"
        mock_backend.get_model_info.assert_called_once()
    
    def test_get_current_backend_info_no_model(self):
        """Test getting current backend info when no model is loaded."""
        info = self.manager.get_current_backend_info()
        assert info is None
    
    def test_get_hardware_info(self):
        """Test getting hardware information."""
        hw_info = self.manager.get_hardware_info()
        
        assert isinstance(hw_info, HardwareInfo)
        assert hw_info.gpu_count == 1
        assert hw_info.total_vram == 8192
        self.mock_hardware_detector.get_hardware_info.assert_called_once()
    
    def test_refresh_backend_availability(self):
        """Test refreshing backend availability."""
        with patch.object(self.manager, '_detect_available_backends') as mock_detect:
            self.manager.refresh_backend_availability()
            mock_detect.assert_called_once()
    
    def test_get_statistics(self):
        """Test getting backend statistics."""
        # Set up some statistics
        self.manager.backend_status["ctransformers"].load_attempts = 10
        self.manager.backend_status["ctransformers"].success_count = 8
        self.manager.backend_status["ctransformers"].failure_count = 2
        self.manager.backend_status["ctransformers"].average_load_time = 2.5
        
        stats = self.manager.get_statistics()
        
        assert isinstance(stats, dict)
        assert "ctransformers" in stats
        
        ctransformers_stats = stats["ctransformers"]
        assert ctransformers_stats["load_attempts"] == 10
        assert ctransformers_stats["success_count"] == 8
        assert ctransformers_stats["failure_count"] == 2
        assert ctransformers_stats["success_rate"] == 0.8
        assert ctransformers_stats["average_load_time"] == 2.5
    
    def test_get_monitoring_report(self):
        """Test getting comprehensive monitoring report."""
        # Mock monitoring components
        mock_performance_stats = {"ctransformers": {"avg_load_time": 2.5}}
        mock_system_metrics = {"cpu_usage": 45.2, "memory_usage": 60.1}
        mock_recent_operations = [
            {
                'backend_name': 'ctransformers',
                'operation': 'load',
                'duration_ms': 2500,
                'success': True,
                'timestamp': time.time()
            }
        ]
        
        with patch.object(self.manager.performance_monitor, 'get_backend_stats', return_value=mock_performance_stats), \
             patch.object(self.manager.monitoring_manager.system_monitor, 'get_current_metrics', return_value=mock_system_metrics), \
             patch.object(self.manager.performance_monitor, 'get_recent_metrics') as mock_recent:
            
            # Mock recent metrics with proper structure
            mock_metric = Mock()
            mock_metric.backend_name = 'ctransformers'
            mock_metric.operation = 'load'
            mock_metric.duration = 2500
            mock_metric.success = True
            mock_metric.start_time = time.time()
            mock_metric.memory_usage_mb = 4096
            mock_metric.error_message = None
            mock_recent.return_value = [mock_metric]
            
            report = self.manager.get_monitoring_report()
        
        assert isinstance(report, dict)
        assert "backend_statistics" in report
        assert "performance_stats" in report
        assert "system_metrics" in report
        assert "hardware_info" in report
        assert "recent_operations" in report
        
        assert report["performance_stats"] == mock_performance_stats
        assert report["system_metrics"] == mock_system_metrics
        assert len(report["recent_operations"]) == 1
    
    def test_callback_registration(self):
        """Test callback registration and triggering."""
        backend_changed_calls = []
        fallback_triggered_calls = []
        loading_progress_calls = []
        
        def on_backend_changed(backend, model_path):
            backend_changed_calls.append((backend, model_path))
        
        def on_fallback_triggered(from_backend, to_backend, error):
            fallback_triggered_calls.append((from_backend, to_backend, error))
        
        def on_loading_progress(message, progress):
            loading_progress_calls.append((message, progress))
        
        # Register callbacks
        self.manager.on_backend_changed = on_backend_changed
        self.manager.on_fallback_triggered = on_fallback_triggered
        self.manager.on_loading_progress = on_loading_progress
        
        # Test backend changed callback
        if self.manager.on_backend_changed:
            self.manager.on_backend_changed("ctransformers", "test.gguf")
        
        assert len(backend_changed_calls) == 1
        assert backend_changed_calls[0] == ("ctransformers", "test.gguf")
        
        # Test fallback triggered callback
        if self.manager.on_fallback_triggered:
            self.manager.on_fallback_triggered("ctransformers", "transformers", "GPU error")
        
        assert len(fallback_triggered_calls) == 1
        assert fallback_triggered_calls[0] == ("ctransformers", "transformers", "GPU error")
        
        # Test loading progress callback
        if self.manager.on_loading_progress:
            self.manager.on_loading_progress("Loading model...", 50)
        
        assert len(loading_progress_calls) == 1
        assert loading_progress_calls[0] == ("Loading model...", 50)
    
    def test_cleanup(self):
        """Test backend manager cleanup."""
        # Set up backends
        mock_backend1 = Mock()
        mock_backend2 = Mock()
        self.manager.backends = {
            "ctransformers": mock_backend1,
            "transformers": mock_backend2
        }
        self.manager.current_backend = mock_backend1
        
        self.manager.cleanup()
        
        # Should unload all backends
        mock_backend1.unload_model.assert_called()
        mock_backend2.unload_model.assert_called()
        
        # Should clear backends dict
        assert len(self.manager.backends) == 0
    
    def test_monitoring_lifecycle(self):
        """Test monitoring system lifecycle."""
        with patch.object(self.manager.monitoring_manager, 'start') as mock_start, \
             patch.object(self.manager.monitoring_manager, 'stop') as mock_stop:
            
            self.manager.start_monitoring()
            mock_start.assert_called_once()
            
            self.manager.stop_monitoring()
            mock_stop.assert_called_once()