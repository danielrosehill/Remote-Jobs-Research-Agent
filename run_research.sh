#!/bin/bash

echo "Starting Company Research Agent..."

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

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Make sure the outputs directory exists
mkdir -p as-agent/outputs

# Run the research agent
echo "Running the company research agent..."
python as-agent/company_research.py
