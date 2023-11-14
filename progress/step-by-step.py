import numpy as np
import sounddevice as sd
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

def play_melody_harmony_and_chord(melody, harmony, chord, sample_rate):
    # Combine melody and harmony into a single stream
    combined = []
    for mel, harm in zip(melody, harmony):
        combined_note = mel + harm  # Assuming melody and harmony are the same length
        combined.append(combined_note)
    combined_audio = np.concatenate(combined)

    # Normalize combined audio to prevent clipping
    combined_audio = combined_audio * (2**15 - 1) / np.max(np.abs(combined_audio))
    combined_audio = combined_audio.astype(np.int16)

    # Play the combined melody and harmony
    sd.play(combined_audio, sample_rate)
    sd.wait()  # Wait until playback is finished

    # Play the chord at the end
    sd.play(chord, sample_rate)
    sd.wait()  # Wait until the chord is finished playing

# Now call the function with the generated melody, harmony, and chord
#play_melody_harmony_and_chord(melody, harmony, chord, SAMPLE_RATE)

import sounddevice as sd
import numpy as np

# Assuming previous definitions and functions (generate_sine_wave, generate_melody, etc.) are in place

# Global variables for tracking playback status within the callback
current_index = 0  # Index for the current frame in the melody/harmony
chord_played = False  # Flag to check if the chord has been played

def play_callback(outdata, frames, time, status):
    global current_index, chord_played
    if status:
        print('Error:', status)

    # Calculate the number of frames per note based on the DURATION constant
    frames_per_note = int(DURATION * SAMPLE_RATE)
    
    # Play melody and harmony until all notes have been played
    if current_index < len(melody) * frames_per_note:
        # Calculate start and end frames for the current note
        start_frame = current_index % frames_per_note
        end_frame = start_frame + frames
        
        # For each frame, add melody and harmony data to the output
        for frame in range(frames):
            note_index = current_index // frames_per_note
            if frame + start_frame < frames_per_note:  # Check if within the current note duration
                outdata[frame] = ((melody[note_index] + harmony[note_index])[frame + start_frame]) / 2
            else:
                outdata[frame] = 0  # Padding with zeros if we are at the end of a note

            current_index += 1  # Move to the next frame
    elif not chord_played:
        # If all melody and harmony notes have been played, play the chord
        outdata[:len(chord)] = chord.reshape(-1, 1)
        outdata[len(chord):] = 0  # Fill the rest of the frames with zeros
        chord_played = True
    else:
        # Once everything has been played, fill with zeros
        outdata.fill(0)

# Set the minimum duration as the shortest note length you have
fast_note_duration = DURATION  # Assuming this is the duration of your fastest note
slow_note_duration = DURATION  # Assuming this is the duration of your slowest note

# Set the sample rate 'fs' to your SAMPLE_RATE constant
fs = SAMPLE_RATE

# Define the stream using the provided configuration and callback
stream = sd.OutputStream(
    channels=1,
    samplerate=fs,
    blocksize=int(min(fast_note_duration, slow_note_duration) * fs),
    callback=play_callback
)

# Use the stream in a context manager to ensure it closes properly
with stream:
    sd.sleep(int((len(melody) + 1) * DURATION * 1000))  # Sleep while the stream is processed