import time
import random
import math
import numpy as np
import pygame

# Constants
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NAMED_SCALES = {
    'major': (2, 2, 1, 2, 2, 2, 1),
    'minor': (2, 1, 2, 2, 1, 2, 2),
    'melodicminor': (2, 1, 2, 2, 2, 2, 1),
    'harmonicminor': (2, 1, 2, 2, 1, 3, 1),
    'pentatonicmajor': (2, 2, 3, 2, 3),
    'bluesmajor': (3, 2, 1, 1, 2, 3),
    'pentatonicminor': (3, 2, 2, 3, 2),
    'bluesminor': (3, 2, 1, 1, 3, 2),
    'augmented': (3, 1, 3, 1, 3, 1),
    'diminished': (2, 1, 2, 1, 2, 1, 2, 1),
    'chromatic': (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    'wholehalf': (2, 1, 2, 1, 2, 1, 2, 1),
    'halfwhole': (1, 2, 1, 2, 1, 2, 1, 2),
    'wholetone': (2, 2, 2, 2, 2, 2),
    'augmentedfifth': (2, 2, 1, 2, 1, 1, 2, 1),
    'japanese': (1, 4, 2, 1, 4),
    'oriental': (1, 3, 1, 1, 3, 1, 2),
    'ionian': (2, 2, 1, 2, 2, 2, 1),
    'dorian': (2, 1, 2, 2, 2, 1, 2),
    'phrygian': (1, 2, 2, 2, 1, 2, 2),
    'lydian': (2, 2, 2, 1, 2, 2, 1),
    'mixolydian': (2, 2, 1, 2, 2, 1, 2),
    'aeolian': (2, 1, 2, 2, 1, 2, 2),
    'locrian': (1, 2, 2, 1, 2, 2, 2),
}

SOLFREGGIO_FREQUENCIES = [174, 285, 396, 417, 528, 639, 741, 852, 963]

def get_scale_notes(key, scale_name):
    scale = NAMED_SCALES[scale_name]
    key_index = NOTES.index(key)
    notes = []
    for interval in scale:
        note_index = (key_index + sum(scale[:interval])) % 12
        notes.append(NOTES[note_index])
    return notes

def play_note(note, frequency, duration):
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    data = np.sin(2 * np.pi * np.arange(num_samples) * frequency / sample_rate)
    data = (data * 32767).astype(np.int16)  # Convert to 16-bit signed integer

    pygame.mixer.init(sample_rate, -16, 1)
    sound = pygame.sndarray.make_sound(data)
    sound.play()
    pygame.time.delay(int(duration * 1000))

def generate_melody(num_iterations=3):
    for _ in range(num_iterations):
        # Choose scale and key
        scale_name = random.choice(list(NAMED_SCALES.keys()))
        key = random.choice(NOTES)
        scale_notes = get_scale_notes(key, scale_name)

        # Choose bpm and duration
        bpm = random.randint(60, 90)  # Meditative and ambient
        duration = 2.0  # Longer note duration

        # Choose frequency
        base_frequency = random.choice(SOLFREGGIO_FREQUENCIES)

        # Play notes on separate timelines
        for note in scale_notes:
            note_frequency = base_frequency * 2 ** ((NOTES.index(note) - NOTES.index('A')) / 12)
            time.sleep(random.uniform(0, duration))
            play_note(note, note_frequency, duration)

        # Apply effects (optional)
        # ...

if __name__ == "__main__":
    generate_melody(num_iterations=5)