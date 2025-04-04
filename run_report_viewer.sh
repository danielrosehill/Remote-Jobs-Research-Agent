#!/bin/bash

echo "Setting up Company Research Report Viewer..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is required but not installed."
    exit 1
fi

# Install dependencies to the existing environment
echo "Installing dependencies..."
pip install -r requirements.txt

# Make sure the outputs directory exists
mkdir -p as-agent/outputs

# Run the Flask app
echo "Starting the report viewer server..."
echo "You can access the reports at http://localhost:5000"
python report_viewer.py
