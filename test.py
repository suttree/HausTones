import pygame
import numpy as np
import math

# Initialize Pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=1)

def generate_sine_wave(frequency, duration):
    """ Generate a sine wave corresponding to a frequency and duration """
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = np.sin(2 * np.pi * frequency * t)
    return (wave * 32767).astype(np.int16)

def generate_xylophone_sound(note_freq):
    """ Generate a xylophone-like sound for a given note """
    duration = 1.0  # 1 second duration
    sine_wave = generate_sine_wave(note_freq, duration)
    return pygame.sndarray.make_sound(sine_wave)

def play_note(note_sound):
    """ Play a single note """
    note_sound.play()

def main():
    # Frequencies for a simple C major scale
    scale_freqs = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]  # C4 to C5

    # Generate xylophone sounds for each note
    notes = [generate_xylophone_sound(freq) for freq in scale_freqs]

    # Play each note in the scale
    for note in notes:
        play_note(note)
        pygame.time.wait(1000)  # Wait for 1 second between notes

    # Keep the program running until all notes have played
    pygame.time.wait(1000)

if __name__ == "__main__":
    main()