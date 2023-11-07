import numpy as np
import sounddevice as sd
import itertools
import time

# Parameters
scale = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]  # C major scale frequencies (C4 to C5)
fs = 44100  # Sampling rate in Hertz
note_duration = 0.5  # Duration of each note in seconds

# Generate a sequence that goes forwards and backwards through the scale
full_scale = scale + scale[-2:0:-1]  # Forward and backward without repeating ends
tone_sequence = itertools.cycle(full_scale)  # Create an iterator that cycles through the sequence

# Function to generate tones with a specific frequency
def generate_tone(frequency, duration, fs):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    tone = np.sin(2 * np.pi * frequency * t)
    return tone

# Callback function for the stream
def callback(outdata, frames, time_info, status):
    global tone_sequence
    if status:
        print(status)
    tone_data = generate_tone(next(tone_sequence), note_duration, fs)
    outdata[:] = tone_data[:frames].reshape(-1, 1)
    if frames < len(tone_data):
        # If the buffer is not filled, append zeros
        outdata[frames:] = 0

# Open an output stream
stream = sd.OutputStream(
    channels=1,
    samplerate=fs,
    blocksize=int(note_duration * fs),  # Set the block size to the note duration
    callback=callback
)

# Start playing the sequence
print("Starting sequence... Press Ctrl+C to stop.")

try:
    with stream:
        input("Press Enter to stop...")
except KeyboardInterrupt:
    pass
finally:
    stream.close()
    print("Sequence stopped.")
