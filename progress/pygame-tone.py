import pygame
import numpy as np
import time
import threading

# Initialize Pygame mixer
pygame.mixer.init(frequency=22050, size=-16, channels=2)

# Constants
SAMPLE_RATE = 22050  # Hertz
DURATION = 0.5  # Seconds
VOLUME = 0.5
REVERB_DELAY = 0.07  # Seconds, delay time for reverb effect
REVERB_DECAY = 0.5  # Decay rate of the reverb effect (volume reduction)

# The C major scale frequencies (in Hertz) for one octave
C_MAJOR_SCALE = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]

# Create a function to generate a note as a numpy array
def generate_note_array(frequency, volume=1.0):
    sample_length = SAMPLE_RATE * DURATION
    t = np.linspace(0, DURATION, int(sample_length), False)
    note = np.sin(frequency * 2 * np.pi * t) * volume
    return note

# Create a function to apply a reverb effect to a note array
def apply_reverb(note_array, delay, decay):
    delay_samples = int(SAMPLE_RATE * delay)
    # Create an empty array to store the note with reverb
    reverb_array = np.zeros(len(note_array) + delay_samples)
    # Copy the original note array into the reverb array
    reverb_array[:len(note_array)] += note_array
    # Add the reverb effect (a delayed and decayed copy of the note)
    reverb_array[delay_samples:] += note_array[:-delay_samples] * decay
    return reverb_array

# A function to play a note using Pygame's mixer
def play_note(frequency, volume=VOLUME, with_reverb=True):
    # Generate the note array
    note_array = generate_note_array(frequency, volume)
    # Apply reverb if desired
    if with_reverb:
        note_array = apply_reverb(note_array, REVERB_DELAY, REVERB_DECAY)
    # Ensure that sound is within the valid range
    note_array = np.int16(note_array * 32767)
    # Create a sound object from this array
    sound = pygame.sndarray.make_sound(note_array)
    # Play sound
    sound.play()

# Function to play a continuous stream of notes
def play_scale(scale):
    while True:  # Loop continuously
        for note_freq in scale:
            play_note(note_freq)
            time.sleep(DURATION)  # Wait for the duration of the note

# Now let's test the functions by playing the C major scale
play_scale_thread = threading.Thread(target=play_scale, args=(C_MAJOR_SCALE,))
play_scale_thread.start()  # Start playing the scale in a separate thread

# Let this run for a few seconds then stop
time.sleep(10)
pygame.mixer.quit()  # Stop the mixer after playing for a while
play_scale_thread.join()  # Ensure the thread has finished before exiting