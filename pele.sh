#!/bin/bash

# Directory containing the files
DIR="melodies"

# Get the full path of the directory
FULL_DIR=$(realpath "$DIR")

# Check if the directory exists
if [ ! -d "$FULL_DIR" ]; then
    echo "Directory $FULL_DIR does not exist."
    exit 1
fi

# Get a list of .py files in the directory
FILES=($FULL_DIR/*.py)

# Check if there are any .py files
if [ ${#FILES[@]} -eq 0 ]; then
    echo "No .py files found in $FULL_DIR."
    exit 1
fi

# Pick a random file
RANDOM_FILE=${FILES[RANDOM % ${#FILES[@]}]}

# Execute the file with Python 3
echo "Running: $RANDOM_FILE"
/usr/bin/env python3 "$RANDOM_FILE"