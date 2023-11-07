import numpy as np
import sounddevice as sd

# Parameters
frequencies = [440, 550, 660]  # Frequencies in Hertz for A, C#, and E respectively
duration = 3.0   # Duration in seconds
fs = 44100       # Sampling rate in Hertz

# Generate time array
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Generate audio signals (sine waves) and sum them
audio = sum(np.sin(2 * np.pi * f * t) for f in frequencies)

# Ensure that the highest value is in the 16-bit range
audio *= 32767 / np.max(np.abs(audio))
audio = audio.astype(np.int16)

# Play audio
sd.play(audio, samplerate=fs)

# Wait for the audio to play before moving on
sd.wait()
