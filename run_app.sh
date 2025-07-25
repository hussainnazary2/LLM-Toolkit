#!/bin/bash
# Launcher script for GGUF Loader App on macOS/Linux

# Make script executable if it isn't already
chmod +x "$0"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    ./setup_env.sh
fi

# Activate virtual environment and run the application
echo "Starting GGUF Loader App..."
source venv/bin/activate
python main.py "$@"

# If there was an error, show the message
if [ $? -ne 0 ]; then
    echo ""
    echo "Application exited with error code $?"
    read -p "Press Enter to continue..."
fi