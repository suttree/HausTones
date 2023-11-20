import numpy as np
import sounddevice as sd
import itertools
import threading

# Define additional scales
scales = {
    'C_major': [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25],
    'G_major': [392.00, 440.00, 493.88, 523.25, 587.33, 659.25, 739.99, 783.99],
    'A_minor': [440.00, 493.88, 523.25, 587.33, 659.25, 698.46, 783.99, 880.00],
    'E_minor': [329.63, 392.00, 415.30, 440.00, 493.88, 587.33, 659.25, 783.99],
    # Add more scales as needed
}

# Select a random scale from the defined scales
import random
scale_name, scale = random.choice(list(scales.items()))
print(f"Selected scale: {scale_name}")

# GTP
# USE PERLIN NOISE TO ADJUST THE DURATION OF fast_note_duration AND slow_note_duration
fs = 44100  # Sampling rate in Hertz
fast_note_duration = 0.36  # Duration of each fast note in seconds
slow_note_duration = 0.73  # Duration of each slow note in seconds

# Generate a sequence that goes forwards and backwards through the scale
full_scale = scale + scale[-2:0:-1]  # Forward and backward without repeating ends
fast_sequence = itertools.cycle(full_scale)  # Fast sequence iterator
slow_sequence = itertools.cycle(full_scale + scale)  # Slow sequence iterator


# GPT
# GENERATE OTHER SEQUENCES USING NOTES FROM THE SCALE,
# AND THEN PICK A RANDOM SEQUENCE
# SEQUENCES SHOULD INCLUDE EITHER ONE OR BOTH OF fast_sequence AND slow_sequence
# SOME SEQUENCES SHOULD ALSO HAVE A THIRD MELODY/HARMONY CALLED mid_sequence
#
# TODO: play a harmonising chord at the end of every slow_sequence iteration
# TODO: add in a mellow bass line
# TODO: add in effects like reverb and delay
#


# Lock for thread safety when accessing the slow sequence
sequence_lock = threading.Lock()

# Function to generate tones with a specific frequency
def generate_tone(frequency, duration, fs):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    tone = np.sin(2 * np.pi * frequency * t)
    return tone

# State for managing current tone and time
current_fast_tone = next(fast_sequence)
current_slow_tone = next(slow_sequence)
fast_elapsed = 0
slow_elapsed = 0

# Callback function for the stream
def callback(outdata, frames, time_info, status):
    global current_fast_tone, current_slow_tone, fast_elapsed, slow_elapsed

    if status:
        print(status)

    # GPT
    # ADD CODE HERE TO GENTLY ALTER fast_note_duration AND slow_note_duration USING PERLIN NOISE
    #

    # Generate tones for the current frame
    fast_tone_data = generate_tone(current_fast_tone, fast_note_duration, fs)[:frames]
    with sequence_lock:  # Ensure thread-safe access to slow_sequence
        slow_tone_data = generate_tone(current_slow_tone, slow_note_duration, fs)[:frames]

    # Mix the fast and slow tones
    mixed_data = fast_tone_data + slow_tone_data
    mixed_data = mixed_data * (0.5 / mixed_data.max())  # Normalize to prevent clipping

    outdata[:] = mixed_data.reshape(-1, 1)

    # Update the elapsed time for each sequence and get new tones if needed
    fast_elapsed += frames
    slow_elapsed += frames

    if fast_elapsed >= int(fast_note_duration * fs):
        fast_elapsed = 0  # Reset elapsed time for the fast sequence
        current_fast_tone = next(fast_sequence)  # Get the next tone in the fast sequence

    if slow_elapsed >= int(slow_note_duration * fs):
        slow_elapsed = 0  # Reset elapsed time for the slow sequence
        with sequence_lock:  # Ensure thread-safe access to slow_sequence
            current_slow_tone = next(slow_sequence)  # Get the next tone in the slow sequence

# Open an output stream
stream = sd.OutputStream(
    channels=1,
    samplerate=fs,
    blocksize=int(min(fast_note_duration, slow_note_duration) * fs),  # Block size set to the shorter duration note
    callback=callback
)

# Start playing the sequence
print("Starting sequences... Press Ctrl+C to stop.")

try:
    with stream:
        input("Press Enter to stop...")
except KeyboardInterrupt:
    pass
finally:
    stream.close()
    print("Sequences stopped.")