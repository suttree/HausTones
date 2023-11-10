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

# Simulated Perlin-like noise adjustment code
def lerp(t, a, b):
    """Linear interpolation between a and b with t"""
    return a + t * (b - a)

def fade(t):
    """Fade function for Perlin noise"""
    return t * t * t * (t * (t * 6 - 15) + 10)

def gradient(h, x):
    """Gradient function based on hash like Perlin noise"""
    h = h & 15
    grad = 1 + (h & 7)  # Gradient value is one of 1, 2, ..., 8
    if h&8:
        grad = -grad  # and a random sign for the gradient
    return grad * x  # Multiply the gradient with x (grad * x)

def perlin(x):
    """Perlin noise at x"""
    # Determine grid cell coordinates
    x0 = int(np.floor(x)) & 255   # & 255 for wraparound in hash table of size 256
    x1 = (x0 + 1) & 255
    # Relative x position in grid cell
    tx = x - np.floor(x)
    # Compute fade curves for x
    u = fade(tx)
    # Hash coordinates of the cube corners
    gx0 = gradient(x0, tx - 0)
    gx1 = gradient(x1, tx - 1)
    # Interpolate the grid point gradients with the fade value
    return lerp(u, gx0, gx1)

# Callback function for the stream
def callback(outdata, frames, time_info, status):
    global current_fast_tone, current_slow_tone, fast_elapsed, slow_elapsed

    if status:
        print(status)


    # Here we simulate the time increment used in Perlin noise
    perlin_time_increment = 0.01  # Increment value for 'time' used in Perlin noise
    time_counter = 0  # Counter to act as time for the Perlin noise function

    # Adjust the note durations based on Perlin noise
    time_counter += perlin_time_increment
    fast_note_duration = np.clip(0.5 + perlin(time_counter) * 0.25, 0.1, 1.0)
    slow_note_duration = np.clip(0.75 + perlin(time_counter + 100) * 0.25, 0.1, 1.5)


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