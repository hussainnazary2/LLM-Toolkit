# llm toolkit

A universal desktop application for loading, managing, and interacting with AI models in all major formats (GGUF, safetensors, PyTorch bin, and Hugging Face models). Built with PySide6 and featuring intelligent backend selection, format detection, and a modular architecture with drag-and-drop addon support.

## Features

- **Universal Model Support**: Load GGUF, safetensors, PyTorch bin files, and Hugging Face models seamlessly
- **Intelligent Backend Selection**: Automatic backend routing based on model format and hardware capabilities
- **LM Studio-like GPU Acceleration**: Automatic GPU detection and seamless CPU fallback
- **Format Detection**: Automatic model format identification and validation
- **Hugging Face Integration**: Direct model loading from Hugging Face Hub with caching
- Clean and intuitive interface for universal model management
- Detailed model information display across all formats
- Enhanced error reporting with actionable solutions
- Memory usage optimization for large models across all backends
- Modular architecture with addon support
- Drag-and-drop addon installation
- Theme customization
- **Smart Hardware Detection**: Automatically uses NVIDIA CUDA, Apple Metal, or AMD ROCm
- **Portable Deployment**: Uses only system-installed drivers, no bundled dependencies

## Requirements

- Python 3.8 or higher
- Windows, macOS, or Linux operating system
- Sufficient RAM for loading AI models (varies by model size and format)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/hussainnazary2/LLM-Toolkit.git
   cd llm-toolkit
   ```

2. Set up the virtual environment:

   **Windows:**
   ```
   setup_env.bat
   ```

   **macOS/Linux:**
   ```
   ./setup_env.sh
   ```

3. **Optional - GPU Acceleration:**
   
   For faster model inference, install GPU support:

   **Windows:**
   ```
   setup_gpu.bat
   ```

   **macOS/Linux:**
   ```
   ./setup_gpu.sh
   ```

   This will automatically detect your GPU and install the appropriate acceleration:
   - **NVIDIA**: CUDA acceleration
   - **AMD**: ROCm acceleration  
   - **Apple**: Metal acceleration (macOS)
   - **Intel**: Vulkan acceleration

   > **Note**: GPU acceleration requires appropriate drivers:
   > - NVIDIA: CUDA 11.8+ or 12.x drivers
   > - AMD: ROCm 5.4+ drivers
   > - Apple: macOS 10.15+ (built-in)
   > - Intel: Latest GPU drivers

4. Activate the virtual environment:

   **Windows:**
   ```
   venv\Scripts\activate
   ```

   **macOS/Linux:**
   ```
   source venv/bin/activate
   ```

## Running the Application

After activating the virtual environment, run the application:

```
python main.py
```

### Quick Start for Judges

To quickly evaluate this project:

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd llm-toolkit
   ```

2. **Windows users:**
   ```cmd
   setup_env.bat
   venv\Scripts\activate
   python main.py
   ```

3. **macOS/Linux users:**
   ```bash
   ./setup_env.sh
   source venv/bin/activate
   python main.py
   ```

The application will launch with a GUI interface for loading and managing AI models. All dependencies are automatically installed during setup.

## Development

### Project Structure

```
llm-toolkit/
├── main.py                  # Application entry point
├── app/
│   ├── core/                # Core application logic (format detection, backend routing)
│   ├── ui/                  # UI components
│   ├── models/              # Data models
│   ├── backends/            # Backend implementations (transformers, llama-cpp-python, etc.)
│   ├── services/            # Services (Hugging Face integration, model loading)
│   └── addons/              # Addon system
├── interfaces/              # Public interfaces
├── utils/                   # Utility functions
├── resources/               # Application resources
└── addons/                  # Directory for installed addons
```

### Running Tests

To run the test suite:

```
python run_tests.py
```

### Creating Addons

Addons must implement the interfaces defined in the `interfaces` directory. See the documentation in the `docs` directory for more information on creating addons.

## License

[MIT License](LICENSE)

## Development with Kiro

This project was developed with significant assistance from Kiro, an AI-powered development assistant. Kiro was instrumental in accelerating development, maintaining code quality, and implementing complex features across the entire stack.

### Architecture & Design
- **Modular Architecture**: Kiro designed the clean separation between backends (`app/backends/`), UI components (`app/ui/`), and core logic (`app/core/`)
  - Example: Created the `BackendInterface` abstraction that allows seamless switching between llama-cpp-python, transformers, and other backends
  - Designed the plugin system in `app/addons/` with drag-and-drop installation support
  
- **Interface Design**: Generated all abstraction interfaces in the `interfaces/` directory
  - `IBackend`: Unified interface for all model backends
  - `IModelLoader`: Standard interface for loading different model formats
  - `IAddon`: Plugin interface for extensibility
  
- **Format Detection System**: Implemented intelligent model format detection in `app/core/format_detector.py`
  - Automatic identification of GGUF, safetensors, PyTorch bin, and Hugging Face models
  - Smart routing to appropriate backends based on file signatures and metadata

### Code Generation & Implementation

#### Backend Implementations
- **`app/backends/llama_backend.py`**: Complete GGUF model support with llama-cpp-python integration
- **`app/backends/transformers_backend.py`**: Hugging Face transformers backend with automatic device mapping
- **`app/backends/safetensors_backend.py`**: Native safetensors format support
- **`app/backends/pytorch_backend.py`**: PyTorch bin file loading and inference

#### UI Components
- **`app/ui/main_window.py`**: Main application window with model management interface
- **`app/ui/model_info_widget.py`**: Detailed model information display supporting all formats
- **`app/ui/addon_manager.py`**: Drag-and-drop addon installation interface
- **Theme System**: Custom theming support with dark/light mode switching

#### Service Layer
- **`app/services/model_loader.py`**: Unified model loading service with format detection and backend routing
- **`app/services/huggingface_service.py`**: Direct Hugging Face Hub integration with caching
- **`app/services/hardware_detector.py`**: Automatic GPU detection (CUDA, Metal, ROCm, Vulkan)

#### Cross-Platform Setup Scripts
- **`setup_env.bat` / `setup_env.sh`**: Automated virtual environment setup for Windows/Unix
- **`setup_gpu.bat` / `setup_gpu.sh`**: Intelligent GPU acceleration installation
  - Detects NVIDIA (CUDA), AMD (ROCm), Apple (Metal), or Intel (Vulkan)
  - Installs appropriate PyTorch and acceleration libraries
  - Handles driver version compatibility

### Testing & Quality Assurance
- **`tests/test_format_detection.py`**: Comprehensive format detection tests
- **`tests/test_backends.py`**: Backend integration tests for all supported formats
- **`tests/test_model_loading.py`**: End-to-end model loading tests
- **`run_tests.py`**: Unified test runner with coverage reporting
- **Error Handling**: Implemented user-friendly error messages with actionable solutions throughout the application

### Development Workflow & Kiro Features Used

#### Specs (`.kiro/specs/`)
Used Kiro's spec system to plan and implement major features:
- Model format detection specification
- Backend architecture design
- Addon system requirements
- GPU acceleration implementation plan

#### File Context
Leveraged Kiro's `#File` and `#Folder` context features to:
- Maintain consistency across related files
- Refactor code while preserving interfaces
- Update multiple backend implementations simultaneously

#### Diagnostics & Debugging
- Used Kiro's diagnostic tools to catch type errors, linting issues, and import problems
- Iteratively fixed cross-platform compatibility issues
- Optimized memory usage for large model loading

### Concrete Examples of Kiro's Impact

1. **Hardware Detection Logic**: Kiro generated the complete GPU detection system that automatically identifies and configures CUDA, Metal, ROCm, or Vulkan acceleration based on available hardware

2. **Format Detection Algorithm**: Implemented sophisticated file signature checking and metadata parsing to accurately identify model formats without user input

3. **Error Recovery**: Created comprehensive error handling that provides users with specific, actionable error messages (e.g., "CUDA not available. Install CUDA 11.8+ drivers or run in CPU mode")

4. **Cross-Platform Scripts**: Generated both Windows batch files and Unix shell scripts with identical functionality, handling path differences and platform-specific commands

5. **Memory Optimization**: Implemented lazy loading and memory-mapped file access for handling models larger than available RAM

### Time Savings & Productivity
- **Rapid Prototyping**: Initial working prototype completed in hours instead of days
- **Multi-Format Support**: Adding each new model format (GGUF, safetensors, PyTorch) took minutes with Kiro's assistance
- **Cross-Platform Testing**: Kiro helped identify and fix platform-specific issues without requiring multiple test machines
- **Documentation**: Generated comprehensive README, API docs, and inline code comments automatically

### Development Philosophy
This project demonstrates how AI-assisted development with Kiro enables:
- Faster iteration on complex features
- Consistent code quality and architecture
- Comprehensive error handling and user experience
- Rapid cross-platform compatibility
- Maintainable, well-documented codebases

The `.kiro/` directory contains specs and development artifacts that showcase the AI-assisted development process, including requirements gathering, design decisions, and implementation planning.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
