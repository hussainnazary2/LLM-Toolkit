"""
Mock objects for testing.
"""

import os
from unittest.mock import MagicMock
from app.models.gguf_model import GGUFModel
from app.models.app_config import AppConfig
from interfaces.i_addon import AddonState, AddonMetadata

class MockGGUFModel:
    """Mock implementation of a GGUF model."""
    
    @staticmethod
    def create_mock(model_id="test-model", name="Test Model", file_path=None):
        """
        Create a mock GGUF model.
        
        Args:
            model_id: ID of the model
            name: Name of the model
            file_path: Path to the model file
            
        Returns:
            Mock GGUFModel instance
        """
        model = MagicMock(spec=GGUFModel)
        model.id = model_id
        model.name = name
        model.file_path = file_path or f"/path/to/{name.lower().replace(' ', '_')}.gguf"
        model.size = 1024 * 1024  # 1 MB
        model.parameters = {
            "model_type": "llama",
            "context_length": 2048,
            "embedding_length": 4096,
            "vocab_size": 32000,
            "num_layers": 32,
            "num_heads": 32
        }
        model.metadata = {
            "description": "Test model for testing",
            "author": "Test Author",
            "license": "MIT",
            "created_at": "2023-01-01"
        }
        model.loaded = False
        model.memory_usage = 0
        
        return model

class MockAddon:
    """Mock implementation of an addon."""
    
    @staticmethod
    def create_mock(addon_id="test-addon", name="Test Addon", version="1.0.0", enabled=True):
        """
        Create a mock addon.
        
        Args:
            addon_id: ID of the addon
            name: Name of the addon
            version: Version of the addon
            enabled: Whether the addon is enabled
            
        Returns:
            Mock addon instance and metadata
        """
        # Create metadata
        metadata_dict = {
            "id": addon_id,
            "name": name,
            "version": version,
            "author": "Test Author",
            "description": f"Test description for {name}",
            "dependencies": [],
            "interfaces": ["test.interface"]
        }
        
        metadata = AddonMetadata.from_dict(metadata_dict)
        
        # Create mock addon instance
        addon = MagicMock()
        addon.get_metadata.return_value = metadata_dict
        addon.initialize.return_value = True
        addon.get_ui_components.return_value = []
        
        # Create state
        state = AddonState.ENABLED if enabled else AddonState.DISABLED
        
        return addon, metadata, state

class MockAppConfig:
    """Mock implementation of application configuration."""
    
    @staticmethod
    def create_mock():
        """
        Create a mock application configuration.
        
        Returns:
            Mock AppConfig instance
        """
        config = MagicMock(spec=AppConfig)
        config.theme = "default"
        config.recent_models = []
        config.window_size = (800, 600)
        config.default_model_dir = os.path.expanduser("~/Documents/GGUF Models")
        config.addon_dir = "addons"
        config.log_level = "INFO"
        
        return config

class MockModelManager:
    """Mock implementation of a model manager."""
    
    @staticmethod
    def create_mock(models=None):
        """
        Create a mock model manager.
        
        Args:
            models: Dictionary of model_id -> model instances
            
        Returns:
            Mock model manager
        """
        from app.core.model_manager import ModelManager
        
        # Create default models if none provided
        if models is None:
            models = {
                "model1": MockGGUFModel.create_mock("model1", "Model 1"),
                "model2": MockGGUFModel.create_mock("model2", "Model 2"),
                "model3": MockGGUFModel.create_mock("model3", "Model 3")
            }
        
        # Create mock manager
        manager = MagicMock(spec=ModelManager)
        
        # Set up methods
        manager.get_all_models.return_value = list(models.keys())
        manager.get_model.side_effect = lambda model_id: models.get(model_id)
        manager.load_model.side_effect = lambda file_path: next(
            (model_id for model_id, model in models.items() if model.file_path == file_path),
            None
        )
        manager.unload_model.return_value = True
        
        return manager

class MockAddonManager:
    """Mock implementation of an addon manager."""
    
    @staticmethod
    def create_mock(addons=None):
        """
        Create a mock addon manager.
        
        Args:
            addons: Dictionary of addon_id -> (addon, metadata, state)
            
        Returns:
            Mock addon manager
        """
        from app.core.addon_manager import AddonManager
        from app.core.addon_registry import AddonRegistry
        from app.core.addon_loader import AddonLoader
        
        # Create default addons if none provided
        if addons is None:
            addons = {
                "addon1": MockAddon.create_mock("addon1", "Addon 1", "1.0.0", True),
                "addon2": MockAddon.create_mock("addon2", "Addon 2", "1.0.0", False),
                "addon3": MockAddon.create_mock("addon3", "Addon 3", "1.0.0", True)
            }
        
        # Create mock registry
        registry = MagicMock(spec=AddonRegistry)
        registry.get_all_addons.return_value = list(addons.keys())
        registry.get_addon_metadata.side_effect = lambda addon_id: addons.get(addon_id, (None, None, None))[1]
        registry.get_addon_state.side_effect = lambda addon_id: addons.get(addon_id, (None, None, None))[2]
        
        # Create mock loader
        loader = MagicMock(spec=AddonLoader)
        
        # Create mock manager
        manager = MagicMock(spec=AddonManager)
        manager.registry = registry
        manager.loader = loader
        
        # Set up methods
        manager.get_addon_instance.side_effect = lambda addon_id: addons.get(addon_id, (None, None, None))[0]
        manager.enable_addon.side_effect = lambda addon_id: (True, None) if addon_id != "addon-error" else (False, "Error enabling addon")
        manager.disable_addon.side_effect = lambda addon_id: (True, None) if addon_id != "addon-error" else (False, "Error disabling addon")
        manager.uninstall_addon.side_effect = lambda addon_id: (True, None) if addon_id != "addon-error" else (False, "Error uninstalling addon")
        
        return manager