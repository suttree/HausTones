import numpy as np
import sounddevice as sd
import time

# Parameters
melody_frequencies = [440, 554.37, 659.25, 880, 440, 659.25, 554.37, 440]  # Melody frequencies in Hertz
bass_frequency = 110  # Bass frequency in Hertz, a lower A (A2)
duration = 0.05   # Shorter duration of each tone in seconds
fs = 44100        # Sampling rate in Hertz
interval = 0.05   # Shorter time interval in seconds between tones

# Generate time array for the full duration
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Function to play a frequency for a certain duration
def play_tone(frequency, duration, volume=1.0):
    # Generate tone
    audio = np.sin(2 * np.pi * frequency * t) * volume
    return audio

# Main loop
try:
    while True:  # Run indefinitely until interrupted
        # Prepare the bass tone and the first melody tone with adjusted volumes
        bass_tone = play_tone(bass_frequency, duration, volume=0.5)
        melody_tone = play_tone(melody_frequencies[0], duration, volume=0.5)

        # Mix the bass and melody tones
        mixed_tone = bass_tone + melody_tone
        # Normalize to prevent clipping after mixing
        mixed_tone *= 32767 / np.max(np.abs(mixed_tone))
        mixed_tone = mixed_tone.astype(np.int16)

        # Play the mixed tone
        sd.play(mixed_tone, samplerate=fs)
        sd.wait()

        # Play the rest of the sequence
        for freq in melody_frequencies[1:]:  # Skip the first note since it's already played
            tone = play_tone(freq, duration)
            # Normalize to prevent clipping
            tone *= 32767 / np.max(np.abs(tone))
            tone = tone.astype(np.int16)

            sd.play(tone, samplerate=fs)
            sd.wait()
            time.sleep(interval)  # Wait for interval time before playing next tone
except KeyboardInterrupt:
    print("Playback interrupted by user")
