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

This project was developed with significant assistance from Kiro, an AI-powered development assistant. Kiro helped with:

### Architecture & Design
- **Modular Architecture**: Kiro assisted in designing the clean separation between backends, UI components, and core logic
- **Interface Design**: Created the abstraction interfaces in the `interfaces/` directory for pluggable backends
- **Format Detection System**: Designed the intelligent model format detection and routing system

### Code Generation & Implementation
- **Backend Implementations**: Generated backend adapters for different model formats (GGUF, safetensors, PyTorch, Hugging Face)
- **UI Components**: Created PySide6 UI components with proper error handling and user feedback
- **Service Layer**: Implemented model loading, caching, and management services
- **Utility Functions**: Generated helper functions for file handling, error management, and hardware detection

### Testing & Quality Assurance
- **Test Suite**: Created comprehensive unit tests, integration tests, and performance tests
- **Error Handling**: Implemented robust error handling with actionable user messages
- **Documentation**: Generated API documentation, user guides, and troubleshooting guides

### Development Workflow
The `.kiro/` directory contains specs and development artifacts that demonstrate the AI-assisted development process, including requirements gathering, design decisions, and implementation planning.

### Key AI Contributions
- Automatic GPU detection and acceleration setup scripts
- Cross-platform compatibility handling (Windows, macOS, Linux)
- Memory optimization for large model loading
- Comprehensive error reporting and user guidance
- Modular addon system architecture

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
