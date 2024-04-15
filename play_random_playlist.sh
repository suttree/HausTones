#!/bin/bash

# Set the directory containing the .wav files
music_dir="post"

# Get the current datetime timestamp
timestamp=$(date +%Y%m%d_%H%M%S)

# Create the playlist file with a random order of .wav files
playlist_file="playlist_${timestamp}.txt"
find "$music_dir" -type f -name "*.wav" | sort -R > "$playlist_file"

# Shuffle and play the playlist using VLC media player (console version)
# RPi
#cvlc --random --playlist-autostart --play-and-exit --one-instance --playlist-tree "$playlist_file"

# OSX
sort -Rsort -R  "$playlist_file" | while IFS= read -r line; do
    afplay "$line"
done
