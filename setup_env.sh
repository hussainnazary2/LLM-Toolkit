#!/bin/bash

echo "Setting up virtual environment for GGUF Loader App..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"
if [ $? -ne 0 ]; then
    echo "Python 3.8 or higher is required. Please update your Python installation."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Virtual environment setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "    source venv/bin/activate"
echo ""
echo "To deactivate the virtual environment, run:"
echo "    deactivate"
echo ""