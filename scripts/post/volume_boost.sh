#!/bin/bash

# Set the volume increase factor
VOLUME_FACTOR=1.5

# Loop through all MP3 files in the current directory
for file in *.mp3; do
    # Check if file exists (this is necessary to handle the case of no MP3 files)
    if [ -f "$file" ]; then
        echo "Processing: $file"
        
        # Generate output filename
        output_file="louder_${file}"
        
        # Run FFmpeg command
        ffmpeg -i "$file" -filter:a "volume=$VOLUME_FACTOR" "$output_file"
        
        echo "Created: $output_file"
        echo "------------------------"
    fi
done

echo "All MP3 files processed."