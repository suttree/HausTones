import numpy as np
import sounddevice as sd
import time

# Parameters
melody_frequencies = [440, 554.37, 659.25, 880, 440, 659.25, 554.37, 440]  # Melody frequencies in Hertz
bass_frequency = 110  # Bass frequency in Hertz, a lower A (A2)
duration = 0.05   # Duration each tone plays in seconds
fs = 44100       # Sampling rate in Hertz
interval = 0.05   # Time interval in seconds between tones
reverb_delay = 0.07  # Delay for the reverb effect in seconds
reverb_decay = 0.5   # Decay factor for the reverb effect

# Generate time array for the full duration
t = np.linspace(0, duration, int(fs * duration), endpoint=False)
# Generate time array for reverb effect (longer to accommodate the delay)
t_reverb = np.linspace(0, duration + reverb_delay, int(fs * (duration + reverb_delay)), endpoint=False)

# Function to play a frequency without reverb
def play_tone(frequency, duration):
    # Generate tone
    audio = np.sin(2 * np.pi * frequency * t)
    # Normalize to 16-bit range
    audio *= 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    # Play audio
    sd.play(audio, samplerate=fs)
    sd.wait()

# Function to play a frequency with a simple reverb effect
def play_tone_with_reverb(frequency, duration):
    # Generate the original tone
    tone = np.sin(2 * np.pi * frequency * t)
    # Generate silence for the reverb delay
    silence = np.zeros(int(reverb_delay * fs))
    # Concatenate the silence to the original tone to create space for the reverb
    tone_with_silence = np.concatenate((tone, silence))
    # Create the reverb effect by adding a delayed and decayed version of the tone
    reverb_effect = np.concatenate((silence, tone)) * reverb_decay
    # Mix the original tone with the reverb effect
    combined_tone = tone_with_silence + reverb_effect
    # Normalize to 16-bit range
    combined_tone *= 32767 / np.max(np.abs(combined_tone))
    combined_tone = combined_tone.astype(np.int16)
    # Play audio
    sd.play(combined_tone, samplerate=fs)
    sd.wait()

# Main loop
try:
    while True:  # Run indefinitely until interrupted
        # Play the bass note with reverb at the start of each sequence
        play_tone_with_reverb(bass_frequency, duration)

        # Play the rest of the sequence without reverb
        for freq in melody_frequencies:  # Play all melody frequencies including the first
            play_tone(freq, duration)
            time.sleep(interval)  # Wait for interval time before playing next tone
except KeyboardInterrupt:
    print("Playback interrupted by user")
