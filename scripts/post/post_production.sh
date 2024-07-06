for f in *.wav; do
    # Convert WAV to MP3
    ffmpeg -i "$f" "${f%.wav}.mp3"
    
    # Apply high-pass and low-pass filters
    ffmpeg -i "${f%.wav}.mp3" -af "highpass=f=200, lowpass=f=3000" "${f%.wav}_filtered.mp3"
    
    # Apply noise reduction
    ffmpeg -i "${f%.wav}_filtered.mp3" -af "afftdn" "${f%.wav}_final.mp3"
    
    # Optional: Remove intermediate files
    rm "${f%.wav}.mp3" "${f%.wav}_filtered.mp3"
done