#!/bin/bash

# Directory containing the files
DIR="melodies"

# Check if the directory exists
if [ ! -d "$DIR" ]; then
    echo "Directory $DIR does not exist."
    exit 1
fi

# Get a list of files in the directory
FILES=($DIR/*)

# Check if there are any files
if [ ${#FILES[@]} -eq 0 ]; then
    echo "No files found in $DIR."
    exit 1
fi

# Pick a random file
RANDOM_FILE=${FILES[RANDOM % ${#FILES[@]}]}

# Execute the file
echo "Running: $RANDOM_FILE"
"$RANDOM_FILE"
