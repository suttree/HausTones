#!/bin/bash

# Set the volume increase factor
VOLUME_FACTOR=1.5

# Loop through all MP3 files in the current directory
for file in *.mp3; do
    # Check if file exists (this is necessary to handle the case of no MP3 files)
    if [ -f "$file" ]; then
        echo "Processing: $file"
        
        # Generate a temporary output filename
        temp_file="${file%.mp3}_temp.mp3"
        
        # Run FFmpeg command
        ffmpeg -i "$file" -filter:a "volume=$VOLUME_FACTOR" "$temp_file"
        
        # Check if the ffmpeg command was successful
        if [ $? -eq 0 ]; then
            # Replace the original file with the processed file
            mv "$temp_file" "$file"
            echo "Processed and replaced: $file"
        else
            echo "Failed to process: $file"
            # Remove the temp file if the processing failed
            rm -f "$temp_file"
        fi
        
        echo "------------------------"
    fi
done

echo "All MP3 files processed."

