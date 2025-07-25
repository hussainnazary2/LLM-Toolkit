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
   git clone https://github.com/yourusername/llm-toolkit.git
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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.