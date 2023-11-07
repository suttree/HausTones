import numpy as np
import sounddevice as sd
import time

# Parameters
scale = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]  # C major scale frequencies (C4 to C5)
fs = 44100  # Sampling rate in Hertz
max_time = 10  # How long to play the chimes in seconds
max_interval = 0.2  # Maximum interval in seconds between notes
phase_increment = 0.01  # How quickly the "wind" changes

# Global variables for keeping track of state
current_phase = 0.0  # Phase for the sine-wave-based interval timing
last_note_time = -max_interval  # Ensures the first note plays immediately
next_frequency = np.random.choice(scale)  # Next note to play
stream_open = True  # Stream state

# Function to generate tones with a specific frequency
def generate_tone(frequency, sample_count):
    t = (np.arange(sample_count) + current_sample) / fs
    tone = np.sin(2 * np.pi * frequency * t)
    return tone

# Callback function for the stream
def callback(outdata, frames, time, status):
    global last_note_time, current_phase, next_frequency, current_sample, stream_open
    if status:
        print(status)
    if not stream_open:  # Stop filling buffer with data if stream is closed
        outdata.fill(0)
        return
    current_time = last_note_time + frames / fs
    interval = (np.sin(current_phase) + 1) / 2 * max_interval
    if (current_time - last_note_time) >= interval:
        # Time for a new note
        outdata[:] = generate_tone(next_frequency, frames).reshape(-1, 1)
        next_frequency = np.random.choice(scale)
        last_note_time = current_time
    else:
        # Continue the previous note
        outdata[:] = generate_tone(next_frequency, frames).reshape(-1, 1)
    current_phase += phase_increment
    current_sample += frames

# Open an output stream
stream = sd.OutputStream(
    channels=1,
    samplerate=fs,
    callback=callback
)

# Start playing the wind chimes
print("Starting wind chime... Press Ctrl+C to stop.")
current_sample = 0  # Current global sample count

with stream:
    time.sleep(max_time)  # Play for a determined duration
    stream_open = False  # Signal to stop the audio stream

print("Wind chime stopped.")
