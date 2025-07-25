# API Reference

Quick reference for all addon interfaces in the GGUF Loader App.

## Core Interfaces

### IAddon

Main interface that all addons must implement.

```python
class IAddon(ABC):
    def initialize(self, app_context) -> bool: ...
    def get_metadata(self) -> AddonMetadata: ...
    def get_interfaces(self) -> List[str]: ...
    def get_ui_components(self) -> List[Any]: ...
    def get_settings(self) -> Dict[str, Any]: ...
    def set_settings(self, settings: Dict[str, Any]) -> bool: ...
    def enable(self) -> bool: ...
    def disable(self) -> bool: ...
    def get_state(self) -> AddonState: ...
    def shutdown(self) -> None: ...
```

### IAddonService

Backend service access for addons.

```python
class IAddonService(ABC):
    def get_current_model(self) -> Optional[GGUFModel]: ...
    def generate_text(self, prompt: str, **kwargs) -> str: ...
    def set_system_prompt(self, prompt: str) -> None: ...
    def get_system_prompt(self) -> str: ...
    def set_temperature(self, temperature: float) -> None: ...
    def get_temperature(self) -> float: ...
    def set_max_tokens(self, max_tokens: int) -> None: ...
    def get_config(self, key: str, default=None) -> Any: ...
    def set_config(self, key: str, value: Any) -> None: ...
```

## Service Interfaces

### IModelService

Direct model service access.

```python
class IModelService(ABC):
    def load_model(self, file_path: str) -> GGUFModel: ...
    def get_current_model(self) -> Optional[GGUFModel]: ...
    def generate(self, prompt: str, system_prompt: str = None, 
                temperature: float = None, max_tokens: int = None) -> str: ...
    def get_model_info(self, model_id: str) -> Dict: ...
    def unload_model(self) -> bool: ...
```

### IChatService

Chat conversation management.

```python
class IChatService(ABC):
    def send_message(self, message: str) -> str: ...
    def get_conversation_history(self) -> List[ChatMessage]: ...
    def clear_conversation(self) -> None: ...
    def set_system_prompt(self, prompt: str) -> None: ...
```

### ISummarizationService

Document summarization services.

```python
class ISummarizationService(ABC):
    def summarize_text(self, text: str, style: str = "concise") -> str: ...
    def summarize_file(self, file_path: str, style: str = "concise") -> str: ...
    def get_supported_formats(self) -> List[str]: ...
```

## Extension Interfaces

### IUIExtension

UI extension capabilities.

```python
class IUIExtension(ABC):
    def get_menu_items(self) -> List[MenuItem]: ...
    def get_toolbar_items(self) -> List[ToolbarItem]: ...
    def get_panels(self) -> List[Panel]: ...
```

### IModelProcessor

Custom model processing.

```python
class IModelProcessor(ABC):
    def get_capabilities(self) -> List[str]: ...
    def get_supported_models(self) -> List[str]: ...
    def can_process(self, model: GGUFModel) -> bool: ...
    def process(self, model: GGUFModel, input_data: Any, 
               options: Optional[Dict[str, Any]] = None) -> ProcessingResult: ...
    def get_input_schema(self) -> Dict[str, Any]: ...
    def get_options_schema(self) -> Dict[str, Any]: ...
```

### IModelProvider

Custom model loading.

```python
class IModelProvider(ABC):
    def load_model(self, file_path: str) -> GGUFModel: ...
    def get_model_info(self, model_id: str) -> Dict[str, Any]: ...
    def unload_model(self, model_id: str) -> bool: ...
```

## Data Classes

### AddonMetadata

```python
class AddonMetadata:
    def __init__(self, id: str, name: str, version: str, author: str, 
                 description: str, website: Optional[str] = None,
                 license: Optional[str] = None, min_app_version: Optional[str] = None,
                 max_app_version: Optional[str] = None, tags: Optional[List[str]] = None,
                 dependencies: Optional[List[str]] = None, 
                 interfaces: Optional[List[str]] = None): ...
```

### MenuItem

```python
class MenuItem:
    def __init__(self, text, callback, parent_menu=None, shortcut=None, icon=None): ...
```

### ToolbarItem

```python
class ToolbarItem:
    def __init__(self, text, callback, icon=None, tooltip=None): ...
```

### Panel

```python
class Panel:
    def __init__(self, title, widget, area="right"): ...
```

### ProcessingResult

```python
class ProcessingResult:
    def __init__(self, success: bool, result: Any = None, 
                 error_message: Optional[str] = None,
                 metrics: Optional[Dict[str, Any]] = None): ...
```

## Enums

### AddonState

```python
class AddonState(Enum):
    DISABLED = auto()
    ENABLED = auto()
    ERROR = auto()
```

## Usage Examples

### Basic Addon

```python
from interfaces import IAddon, AddonMetadata, AddonState

class MyAddon(IAddon):
    def initialize(self, app_context) -> bool:
        return True
    
    def get_metadata(self) -> AddonMetadata:
        return AddonMetadata(
            id="my_addon",
            name="My Addon",
            version="1.0.0",
            author="Developer",
            description="My custom addon"
        )
    
    # ... implement other methods
```

### Service Access

```python
def initialize(self, app_context) -> bool:
    self.addon_service = app_context.get_service('addon_service')
    
    # Generate text
    response = self.addon_service.generate_text("Hello, AI!")
    
    # Configure AI
    self.addon_service.set_temperature(0.7)
    self.addon_service.set_system_prompt("You are a helpful assistant.")
    
    return True
```

### UI Extension

```python
from interfaces import IUIExtension, MenuItem

class MyUIAddon(IAddon, IUIExtension):
    def get_menu_items(self) -> List[MenuItem]:
        return [
            MenuItem("My Action", self.my_action, "Addons", "Ctrl+M")
        ]
    
    def my_action(self):
        print("Menu action triggered!")
```