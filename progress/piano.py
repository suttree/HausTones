import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Define musical keys and scales
KEYS = ["C", "D", "E", "F", "G", "A", "B"]
SCALES = {
    "Major": [0, 2, 4, 5, 7, 9, 11],
    "Minor": [0, 2, 3, 5, 7, 8, 10],
    # Add more scales as needed
}

# Set the tempo in BPM (beats per minute)
tempo = 60

# Function to generate a random melody in the chosen scale
def generate_melody(key, scale):
    melody = []
    num_notes = random.randint(8, 16)  # Random number of notes
    for _ in range(num_notes):
        if scale:  # Check if the scale is not empty
            note_index = random.randint(0, len(scale) - 1)
            note = key + KEYS[scale[note_index] % len(KEYS)]  # Ensure the note index wraps around
            melody.append(note)
    return melody


# Function to generate a harmony for the melody
# Function to generate a harmony for the melody
def generate_harmony(melody, scale):
    harmony = []
    for note in melody:
        note_index = scale.index(note[-1]) if note[-1] in scale else -1  # Check if the note is in the scale
        if note_index != -1:
            harmony_note_index = (note_index + 2) % len(scale)  # Create a simple harmony by shifting two steps in the scale
            harmony_note = note[:-1] + KEYS[scale[harmony_note_index]]
            harmony.append(harmony_note)
    return harmony


# Choose a random key and scale
key = random.choice(KEYS)
scale_name, scale_values = random.choice(list(SCALES.items()))

# Generate melody and harmony
melody = generate_melody(key, scale_values)
harmony = generate_harmony(melody, scale_values)

# Print the chosen key, scale, melody, and harmony
print(f"Key: {key}")
print(f"Scale: {scale_name}")
print(f"Melody: {melody}")
print(f"Harmony: {harmony}")

# Set up Pygame for audio playback
pygame.mixer.init()
pygame.mixer.set_num_channels(1)  # Set the number of audio channels

# Function to play a note
def play_note(note):
    pygame.mixer.Sound(f"piano/{note}.wav").play()  # Replace with the path to your piano samples

# Play the melody and harmony
for note in melody:
    play_note(note)
    time.sleep(60 / tempo)  # Sleep for the duration of one beat
for note in harmony:
    play_note(note)
    time.sleep(60 / tempo)

# Wait for the audio to finish
pygame.time.delay(int((len(melody) + len(harmony)) * 60000 / tempo))

# Quit Pygame
pygame.quit()
