for f in *.mp3; do ffmpeg -i "$f" -af "highpass=f=200, lowpass=f=3000" "${f}_filtered.mp3"; done 

for f in *.mp3; do ffmpeg -i "${f}_filtered.mp3" -af "afftdn" "${f}_final.mp3"; done
