import numpy as np
import sounddevice as sd
import time

# Parameters
frequencies = [440, 550, 660]  # Frequencies in Hertz for A, C#, and E respectively
duration = 0.25   # Duration each tone plays in seconds
fs = 44100       # Sampling rate in Hertz
interval = 0.25   # Time interval in seconds between tones

# Generate time array for the full duration
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Function to play a frequency for a certain duration
def play_tone(frequency, duration):
    # Generate tone
    audio = np.sin(2 * np.pi * frequency * t)
    # Normalize to 16-bit range
    audio *= 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    # Play audio
    sd.play(audio, samplerate=fs)
    sd.wait()  # Wait for the audio to play before moving on

# Play each frequency after a specific interval
for freq in frequencies:
    play_tone(freq, duration)
    time.sleep(interval)  # Wait for interval time before playing next tone
