#!/bin/bash

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null
then
    echo "ffmpeg could not be found. Please install ffmpeg to use this script."
    exit 1
fi

# Find all .wav files in the current directory
wavfiles=$(find . -maxdepth 1 -type f -name "*.wav")

# Check if any .wav files are found
if [ -z "$wavfiles" ]; then
    echo "No .wav files found in the current directory."
    exit 1
fi

# Loop through each .wav file and convert it to .mp3
for wavfile in $wavfiles
do
    # Get the filename without the extension
    filename=$(basename "$wavfile" .wav)
    
    # Convert to mp3
    ffmpeg -i "$wavfile" -codec:a libmp3lame -qscale:a 2 "${filename}.mp3"
    
    # Check if the conversion was successful
    if [ $? -eq 0 ]; then
        echo "Successfully converted $wavfile to ${filename}.mp3"
    else
        echo "Failed to convert $wavfile"
    fi
done

