"""
Pytest configuration and fixtures for backend testing.

This module provides common fixtures and configuration for all backend tests.
"""

import os
import sys
import tempfile
import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock
from typing import Dict, Any, List

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

# Import core modules
from core.model_backends import (
    BackendConfig, BackendType, HardwareInfo, LoadingResult, 
    GenerationConfig, ModelBackend, HardwareType
)
from core.hardware_detector import HardwareDetector, GPUDevice
from core.backend_manager import BackendManager


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def mock_model_file(temp_dir):
    """Create a mock GGUF model file for testing."""
    model_path = temp_dir / "test_model.gguf"
    
    # Create a minimal GGUF-like file with header
    with open(model_path, 'wb') as f:
        f.write(b'GGUF')  # GGUF magic number
        f.write(b'\x00' * 1020)  # Padding to make it 1KB
        f.write(b'test model data' * 100)  # Some content
    
    return model_path


@pytest.fixture
def large_mock_model_file(temp_dir):
    """Create a large mock model file for testing memory scenarios."""
    model_path = temp_dir / "large_model.gguf"
    
    # Create a 100MB mock file
    with open(model_path, 'wb') as f:
        f.write(b'GGUF')  # GGUF magic number
        f.write(b'\x00' * (100 * 1024 * 1024 - 4))  # 100MB - 4 bytes
    
    return model_path


@pytest.fixture
def backend_config():
    """Create a default backend configuration."""
    return BackendConfig(
        name="test_backend",
        enabled=True,
        gpu_enabled=True,
        gpu_layers=-1,
        context_size=4096,
        batch_size=512,
        threads=-1
    )


@pytest.fixture
def generation_config():
    """Create a default generation configuration."""
    return GenerationConfig(
        max_tokens=256,
        temperature=0.7,
        top_p=0.9,
        top_k=40,
        repeat_penalty=1.1,
        seed=42,
        stop_sequences=["</s>"],
        stream=False
    )


@pytest.fixture
def mock_gpu_device():
    """Create a mock GPU device."""
    return GPUDevice(
        id=0,
        name="Test GPU",
        vendor="nvidia",
        memory_mb=8192,
        driver_version="11.8",
        compute_capability="8.6",
        supports_cuda=True,
        supports_rocm=False,
        supports_opencl=True,
        supports_vulkan=True,
        supports_metal=False
    )


@pytest.fixture
def mock_hardware_info(mock_gpu_device):
    """Create mock hardware information."""
    return HardwareInfo(
        gpu_count=1,
        gpu_devices=[{
            'id': mock_gpu_device.id,
            'name': mock_gpu_device.name,
            'vendor': mock_gpu_device.vendor,
            'memory_mb': mock_gpu_device.memory_mb,
            'driver_version': mock_gpu_device.driver_version,
            'compute_capability': mock_gpu_device.compute_capability,
            'supports_cuda': mock_gpu_device.supports_cuda,
            'supports_rocm': mock_gpu_device.supports_rocm,
            'supports_opencl': mock_gpu_device.supports_opencl,
            'supports_vulkan': mock_gpu_device.supports_vulkan,
            'supports_metal': mock_gpu_device.supports_metal
        }],
        total_vram=8192,
        cpu_cores=8,
        total_ram=16384,
        recommended_backend="ctransformers",
        supported_hardware=[HardwareType.CPU, HardwareType.CUDA, HardwareType.OPENCL]
    )


@pytest.fixture
def mock_hardware_detector(mock_hardware_info, mock_gpu_device):
    """Create a mock hardware detector."""
    detector = Mock(spec=HardwareDetector)
    detector.detect_gpus.return_value = [mock_gpu_device]
    detector.detect_cpu_info.return_value = {
        'cores': 8,
        'threads': 16,
        'frequency': 3200,
        'architecture': 'x86_64',
        'processor': 'Test CPU'
    }
    detector.detect_system_memory.return_value = {
        'total': 16384,
        'available': 12288,
        'used': 4096,
        'percent': 25.0
    }
    detector.get_hardware_info.return_value = mock_hardware_info
    detector.get_optimal_settings.return_value = {
        'gpu_enabled': True,
        'gpu_layers': -1,
        'context_size': 4096,
        'batch_size': 512,
        'threads': 8
    }
    detector.benchmark_backend.return_value = {
        'load_time': 2.5,
        'inference_speed': 15.2,
        'memory_usage': 4096,
        'tokens_per_second': 25.8
    }
    return detector


@pytest.fixture
def cpu_only_hardware_info():
    """Create hardware info for CPU-only systems."""
    return HardwareInfo(
        gpu_count=0,
        gpu_devices=[],
        total_vram=0,
        cpu_cores=4,
        total_ram=8192,
        recommended_backend="llamafile",
        supported_hardware=[HardwareType.CPU]
    )


@pytest.fixture
def amd_gpu_hardware_info():
    """Create hardware info for AMD GPU systems."""
    amd_gpu = {
        'id': 0,
        'name': "AMD Radeon RX 7900 XTX",
        'vendor': "amd",
        'memory_mb': 24576,
        'driver_version': "23.11.1",
        'compute_capability': None,
        'supports_cuda': False,
        'supports_rocm': True,
        'supports_opencl': True,
        'supports_vulkan': True,
        'supports_metal': False
    }
    
    return HardwareInfo(
        gpu_count=1,
        gpu_devices=[amd_gpu],
        total_vram=24576,
        cpu_cores=16,
        total_ram=32768,
        recommended_backend="ctransformers",
        supported_hardware=[HardwareType.CPU, HardwareType.ROCM, HardwareType.OPENCL, HardwareType.VULKAN]
    )


@pytest.fixture
def multi_gpu_hardware_info():
    """Create hardware info for multi-GPU systems."""
    gpu1 = {
        'id': 0,
        'name': "NVIDIA RTX 4090",
        'vendor': "nvidia",
        'memory_mb': 24576,
        'driver_version': "535.98",
        'compute_capability': "8.9",
        'supports_cuda': True,
        'supports_rocm': False,
        'supports_opencl': True,
        'supports_vulkan': True,
        'supports_metal': False
    }
    
    gpu2 = {
        'id': 1,
        'name': "NVIDIA RTX 4090",
        'vendor': "nvidia",
        'memory_mb': 24576,
        'driver_version': "535.98",
        'compute_capability': "8.9",
        'supports_cuda': True,
        'supports_rocm': False,
        'supports_opencl': True,
        'supports_vulkan': True,
        'supports_metal': False
    }
    
    return HardwareInfo(
        gpu_count=2,
        gpu_devices=[gpu1, gpu2],
        total_vram=49152,
        cpu_cores=24,
        total_ram=65536,
        recommended_backend="ctransformers",
        supported_hardware=[HardwareType.CPU, HardwareType.CUDA, HardwareType.OPENCL, HardwareType.VULKAN]
    )


class MockBackend(ModelBackend):
    """Mock backend implementation for testing."""
    
    def __init__(self, config: BackendConfig, available: bool = True, load_success: bool = True):
        super().__init__(config)
        self._available = available
        self._load_success = load_success
        self._generation_calls = []
        self._load_calls = []
        self._unload_calls = []
    
    def is_available(self):
        if self._available:
            return True, None
        else:
            return False, "Mock backend not available"
    
    def load_model(self, model_path: str, **kwargs):
        self._load_calls.append((model_path, kwargs))
        
        if not self._load_success:
            return LoadingResult(
                success=False,
                backend_used=self.config.name,
                hardware_used="cpu",
                load_time=0.5,
                error_message="Mock loading failure"
            )
        
        # Validate model path
        is_valid, error = self.validate_model_path(model_path)
        if not is_valid:
            return LoadingResult(
                success=False,
                backend_used=self.config.name,
                hardware_used="cpu",
                load_time=0.1,
                error_message=error
            )
        
        self.model_path = model_path
        self.is_loaded = True
        self.load_time = 1.5
        self.memory_usage = 2048
        
        return LoadingResult(
            success=True,
            backend_used=self.config.name,
            hardware_used="cuda" if self.config.gpu_enabled else "cpu",
            load_time=self.load_time,
            memory_usage=self.memory_usage,
            model_info={
                'model_type': 'llama',
                'context_length': self.config.context_size,
                'gpu_layers': self.config.gpu_layers if self.config.gpu_enabled else 0
            }
        )
    
    def generate_text(self, prompt: str, config: GenerationConfig):
        if not self.is_loaded:
            raise ModelLoadingError("No model loaded")
        
        self._generation_calls.append((prompt, config))
        return f"Mock response to: {prompt[:50]}..."
    
    def unload_model(self):
        self._unload_calls.append(True)
        self.is_loaded = False
        self.model_path = None
        return True
    
    def get_hardware_info(self):
        return HardwareInfo(
            gpu_count=1 if self.config.gpu_enabled else 0,
            total_vram=8192 if self.config.gpu_enabled else 0,
            cpu_cores=8,
            total_ram=16384,
            recommended_backend=self.config.name,
            supported_hardware=[HardwareType.CPU, HardwareType.CUDA] if self.config.gpu_enabled else [HardwareType.CPU]
        )


@pytest.fixture
def mock_backend_factory():
    """Factory for creating mock backends with different configurations."""
    def create_mock_backend(name: str, available: bool = True, load_success: bool = True, **config_kwargs):
        config = BackendConfig(name=name, **config_kwargs)
        return MockBackend(config, available=available, load_success=load_success)
    
    return create_mock_backend


@pytest.fixture
def performance_test_data():
    """Test data for performance benchmarking."""
    return {
        'small_prompt': "Hello, how are you?",
        'medium_prompt': "Write a detailed explanation of machine learning concepts including supervised learning, unsupervised learning, and reinforcement learning.",
        'large_prompt': "Create a comprehensive technical documentation for a software project that includes architecture overview, API documentation, installation instructions, usage examples, troubleshooting guide, and performance optimization tips. The documentation should be well-structured and include code examples in multiple programming languages." * 3,
        'code_prompt': "def fibonacci(n):\n    # Complete this function to calculate fibonacci numbers",
        'chat_prompt': "User: What is the capital of France?\nAssistant: The capital of France is Paris.\nUser: What about Germany?",
    }


@pytest.fixture
def benchmark_configs():
    """Different configurations for benchmarking."""
    return {
        'fast': GenerationConfig(max_tokens=50, temperature=0.1),
        'balanced': GenerationConfig(max_tokens=256, temperature=0.7),
        'creative': GenerationConfig(max_tokens=512, temperature=0.9, top_p=0.95),
        'precise': GenerationConfig(max_tokens=100, temperature=0.1, top_k=10),
    }


# Test markers for different test categories
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration
pytest.mark.performance = pytest.mark.performance
pytest.mark.mock = pytest.mark.mock
pytest.mark.slow = pytest.mark.slow
pytest.mark.gpu_required = pytest.mark.gpu_required