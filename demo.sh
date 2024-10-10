#!/bin/bash

# Directory containing the .wav files
DIR="demo"

# Check if the directory exists
if [ -d "$DIR" ]; then
  # Loop through all .wav files in the directory
  for file in "$DIR"/*.wav; do
    # Check if there are any .wav files in the directory
    if [ -e "$file" ]; then
      echo "Playing: $file"
      aplay "$file"
    else
      echo "No .wav files found in the $DIR directory."
      exit 1
    fi
  done
else
  echo "Directory $DIR does not exist."
  exit 1
fi

