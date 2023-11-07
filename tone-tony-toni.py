import numpy as np
import sounddevice as sd
import time

# Parameters
scale = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]  # C major scale frequencies (C4 to C5)
fs = 44100  # Sampling rate in Hertz
base_duration = 1.0  # Base duration in seconds for a tone
max_interval = 1.5  # Max interval in seconds between successive tones
attack_duration = 0.1  # Duration of the attack (fade-in) in seconds
release_duration = 0.3  # Duration of the release (fade-out) in seconds

# Generate a tone with a specific frequency and duration
def generate_tone(frequency, duration, fs, attack_duration, release_duration):
    # Generate time array
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    # Create the envelope
    envelope = np.ones_like(t)
    attack_samples = int(attack_duration * fs)
    release_samples = int(release_duration * fs)
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)  # Attack
    envelope[-release_samples:] = np.linspace(1, 0, release_samples)  # Release
    # Generate the tone with the envelope applied
    tone = np.sin(2 * np.pi * frequency * t) * envelope
    return tone

# Function to play a frequency
def play_tone(frequency, duration):
    tone = generate_tone(frequency, duration, fs, attack_duration, release_duration)
    tone *= 32767 / np.max(np.abs(tone))  # Normalize the tone's volume
    tone = tone.astype(np.int16)  # Convert to 16-bit format
    sd.play(tone, samplerate=fs)
    sd.wait()  # Wait for the tone to finish

def wind_chime():
    last_play_time = time.time() - max_interval  # Initialize with an offset to play immediately
    while True:
        current_time = time.time()
        # Check if it's time to play a new tone based on a sine wave interval
        if current_time - last_play_time > (np.sin(current_time) + 1) / 2 * max_interval:
            # Randomly select a frequency from the scale
            frequency = np.random.choice(scale)
            # Randomize duration to vary the sound
            duration = np.random.uniform(0.3, base_duration)
            play_tone(frequency, duration)
            last_play_time = current_time

# Run the wind chime in a try-except block to catch KeyboardInterrupt
try:
    print("Starting wind chime... Press Ctrl+C to stop.")
    wind_chime()
except KeyboardInterrupt:
    print("Wind chime stopped by user.")
