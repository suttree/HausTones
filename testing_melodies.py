import numpy as np
from scipy.io.wavfile import write
import random

# Redefine the constants and note frequencies
SAMPLE_RATE = 44100  # Hertz
DURATION = 0.5  # Seconds
NOTE_FREQUENCIES = {
    'C4': 261.63,
    'C#4/Db4': 277.18,
    'D4': 293.66,
    'D#4/Eb4': 311.13,
    'E4': 329.63,
    'F4': 349.23,
    'F#4/Gb4': 369.99,
    'G4': 392.00,
    'G#4/Ab4': 415.30,
    'A4': 440.00,
    'A#4/Bb4': 466.16,
    'B4': 493.88
}

# Define the musical keys and scales
MUSICAL_KEYS = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F']
SCALES = {
    'major': ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4'],
    'minor': ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4']
}

# Redefine the functions for generating waves and saving files
def generate_sine_wave(freq, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    note = np.sin(freq * t * 2 * np.pi)
    audio = note * (2**15 - 1) / np.max(np.abs(note))
    audio = audio.astype(np.int16)
    return audio

def save_audio(audio_data, filename):
    write(filename, SAMPLE_RATE, audio_data)

def generate_melody(scale_notes, bpm):
    melody = []
    beats_per_second = bpm / 60
    duration_per_note = 1 / beats_per_second
    
    for _ in range(4):  # Generate 4 notes for the melody
        note = random.choice(scale_notes)
        frequency = NOTE_FREQUENCIES[note]
        audio_data = generate_sine_wave(frequency, DURATION, SAMPLE_RATE)
        melody.append(audio_data)
        
    return melody

def generate_harmony(melody, scale_notes):
    harmony = []
    for note in melody:
        harmony_note = random.choice([n for n in scale_notes if n not in note])
        frequency = NOTE_FREQUENCIES[harmony_note]
        audio_data = generate_sine_wave(frequency, DURATION, SAMPLE_RATE)
        harmony.append(audio_data)
    return harmony

def generate_chord(scale_notes):
    chord_notes = random.sample(scale_notes, 3)  # Choose 3 random notes for the chord
    chord_data = np.zeros((int(SAMPLE_RATE * DURATION),), dtype=np.int16)
    for note in chord_notes:
        frequency = NOTE_FREQUENCIES[note]
        audio_data = generate_sine_wave(frequency, DURATION, SAMPLE_RATE)
        chord_data += audio_data
    chord_data = chord_data // len(chord_notes)  # Average the chord data
    return chord_data

# Choose a random key and scale
key = random.choice(MUSICAL_KEYS)
scale_name = random.choice(list(SCALES.keys()))
scale_notes = SCALES[scale_name]

# Generate the melody, harmony, and chord
melody = generate_melody(scale_notes, 60)
harmony = generate_harmony(melody, scale_notes)
chord = generate_chord(scale_notes)

# Save the generated sounds to files
melody_files = []
harmony_files = []

for i, (melody_note, harmony_note) in enumerate(zip(melody, harmony

