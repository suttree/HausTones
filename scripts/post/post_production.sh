for f in *.mp3; do
    
    # Apply high-pass and low-pass filters
    ffmpeg -i "${f%}.mp3" -af "highpass=f=200, lowpass=f=3000" "${f%}_filtered.mp3"
    
    # Apply noise reduction
    ffmpeg -i "${f%.wav}_filtered.mp3" -af "afftdn" "${f%.wav}_final.mp3"
    
    # Optional: Remove intermediate files
    rm "${f%.wav}.mp3" "${f%.wav}_filtered.mp3"
done
