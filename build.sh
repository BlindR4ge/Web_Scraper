#!/bin/bash

pip install -r requirements.txt

SOURCE_FILES=(
    sql-generator.py
    web_scraper.py
)

OUTPUT_FILE=project.py

BUILD_COMMAND="python3 -m py_compile ${SOURCE_FILES[*]}"

if ! command -v python3 -m py_compile &> /dev/null; then
    echo "Error: py_compile command not found. Make sure Python 3 is installed."
    exit 1
fi

echo "Building project..."
if $BUILD_COMMAND; then
    echo "Project built successfully."
else
    echo "Error: Failed to build project."
    exit 1
fi

mv __pycache__/${SOURCE_FILES[0]%.py}.cpython-*.pyc $OUTPUT_FILE

echo "Build completed."