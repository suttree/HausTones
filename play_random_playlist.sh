#!/bin/bash

# Set the directory containing the .wav files
music_dir="post"

# Get the current datetime timestamp
timestamp=$(date +%Y%m%d_%H%M%S)

# Create the playlist file with a random order of .wav files
playlist_file="playlist_${timestamp}.txt"
find "$music_dir" -type f -name "*.wav" | sort -R > "$playlist_file"

# Rpi
sort -Rsort -R  "$playlist_file" | while IFS= read -r line; do
    aplay "$line"
done

# OSX
sort -Rsort -R  "$playlist_file" | while IFS= read -r line; do
    afplay "$line"
done
