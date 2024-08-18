#!/bin/bash

# First pass: Analyze audio files
for file in *.mp3; do
    ffmpeg -i "$file" -af "loudnorm=print_format=json" -f null - 2>&1 | tail -n 12 > "${file%.mp3}.loudnorm"
done

# Second pass: Apply normalization
for file in *.mp3; do
    measured_I=$(grep '"input_i" :' "${file%.mp3}.loudnorm" | awk -F: '{print $2}' | tr -d ' ",')
    measured_LRA=$(grep '"input_lra" :' "${file%.mp3}.loudnorm" | awk -F: '{print $2}' | tr -d ' ",')
    measured_TP=$(grep '"input_tp" :' "${file%.mp3}.loudnorm" | awk -F: '{print $2}' | tr -d ' ",')
    measured_thresh=$(grep '"input_thresh" :' "${file%.mp3}.loudnorm" | awk -F: '{print $2}' | tr -d ' ",')

    ffmpeg -i "$file" -af "loudnorm=I=-14:LRA=11:TP=-1:measured_I=$measured_I:measured_LRA=$measured_LRA:measured_TP=$measured_TP:measured_thresh=$measured_thresh:linear=true:print_format=summary" -c:a libmp3lame -q:a 2 "normalized_${file}"

    echo "Normalized: $file"
    rm "${file%.mp3}.loudnorm"
done

echo "All MP3 files normalized."