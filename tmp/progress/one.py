import pygame
import numpy as np
import time

# Initialize Pygame Mixer
pygame.mixer.init()

# Frequencies for a C major scale in Hz
frequencies = {'C': 261.63, 'D': 293.66, 'E': 329.63, 'F': 349.23, 'G': 392.00, 'A': 440.00, 'B': 493.88}

def generate_tone(frequency, duration):
    # Generate a sine wave for the given frequency and duration
    sample_rate = 44100  # Audio CD quality
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = np.sin(2 * np.pi * frequency * t)
    return wave

def play_tone(wave):
    # Convert the wave into an array of 16-bit integers
    sound_wave = np.array(wave * 32767, dtype=np.int16)
    sound = pygame.sndarray.make_sound(sound_wave)
    sound.play()
    time.sleep(sound.get_length())  # Wait for the sound to finish playing

# Play each note in the scale in a loop
while True:
    for note in frequencies:
        wave = generate_tone(frequencies[note], 0.5)  # 0.5 seconds duration for each note
        play_tone(wave)
