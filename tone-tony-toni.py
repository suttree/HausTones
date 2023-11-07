import numpy as np
import sounddevice as sd
import time

# Parameters
scale = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]  # C major scale frequencies (C4 to C5)
bass_scale = [130.81, 146.83, 164.81]  # Some bass frequencies (C3, D3, E3)
fs = 44100  # Sampling rate in Hertz
max_interval = 0.2  # Maximum interval in seconds between notes
phase_increment = 0.01  # How quickly the "wind" changes
tone_counter = 0  # Count the number of tones played

# Global variables for keeping track of state
current_phase = 0.0  # Phase for the sine-wave-based interval timing
next_frequency = np.random.choice(scale)  # Next note to play

# Function to generate tones with a specific frequency
def generate_tone(frequency, sample_count):
    t = (np.arange(sample_count) / fs)
    tone = np.sin(2 * np.pi * frequency * t)
    return tone

# Callback function for the stream
def callback(outdata, frames, time_info, status):
    global current_phase, next_frequency, tone_counter
    if status:
        print(status)
    interval = (np.sin(current_phase) + 1) / 2 * max_interval
    # Fill the output buffer with the current frequency tone
    tone_data = generate_tone(next_frequency, frames)
    if tone_counter % 12 == 0:  # Play bass note on every 12th tone
        bass_frequency = np.random.choice(bass_scale)
        bass_data = generate_tone(bass_frequency, frames)
        tone_data += bass_data  # Add bass tone to the normal tone for overlap
    outdata[:] = tone_data.reshape(-1, 1)
    # Update phase and frequency at intervals based on the sine wave
    current_time = time_info.outputBufferDacTime
    if (current_time % interval) < (frames / fs):
        current_phase += phase_increment
        if current_phase >= (2 * np.pi):
            current_phase = 0
        next_frequency = np.random.choice(scale)
        tone_counter += 1

# Normalize and prevent clipping in the callback
def safe_normalize(samples):
    peak = np.max(np.abs(samples))
    if peak > 0:
        return samples / peak
    return samples

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
