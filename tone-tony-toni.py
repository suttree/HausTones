import numpy as np
import sounddevice as sd
import time

# Parameters
scale = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]  # C major scale frequencies (C4 to C5)
fs = 44100  # Sampling rate in Hertz
max_interval = 0.5  # Maximum interval in seconds between notes
phase_increment = 0.01  # How quickly the "wind" changes

# Global variables for keeping track of state
current_phase = 0.0  # Phase for the sine-wave-based interval timing
next_frequency = np.random.choice(scale)  # Next note to play

# Function to generate tones with a specific frequency
def generate_tone(frequency, sample_count):
    t = (np.arange(sample_count) / fs)
    tone = np.sin(2 * np.pi * frequency * t)
    return tone

# Callback function for the stream
def callback(outdata, frames, time, status):
    global current_phase, next_frequency
    if status:
        print(status)
    current_time = time.outputBufferDacTime
    interval = (np.sin(current_phase) + 1) / 2 * max_interval
    # Fill the output buffer with the current frequency tone
    outdata[:] = generate_tone(next_frequency, frames).reshape(-1, 1)
    # Update phase and frequency at intervals based on the sine wave
    if (current_time % interval) < (frames / fs):
        current_phase += phase_increment
        if current_phase >= (2 * np.pi):
            current_phase -= (2 * np.pi)
        next_frequency = np.random.choice(scale)

# Open an output stream
stream = sd.OutputStream(
    channels=1,
    samplerate=fs,
    callback=callback
)

# Start playing the wind chimes
print("Starting wind chime... Press Ctrl+C to stop.")

try:
    with stream:
        while True:  # Infinite loop to keep the stream open
            time.sleep(0.1)
except KeyboardInterrupt:
    print("Wind chime stopped by user.")
