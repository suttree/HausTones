import pygame
import time
import math

# Initialize Pygame Mixer
pygame.mixer.init()

# Function to generate a major scale based on the root frequency
def generate_major_scale(root_freq):
    ratios = [1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8]  # Ratios for a major scale
    return [root_freq * ratio for ratio in ratios]

# Function to play a sound for a given frequency
def play_frequency(frequency, duration=0.5):
    # Generate a sound for a given frequency and duration
    sample_rate = 44100  # Audio CD quality
    n_samples = int(sample_rate * duration)
    buf = [int(4096 * math.sin(2 * math.pi * frequency * x / sample_rate)) for x in range(n_samples)]
    sound = pygame.sndarray.make_sound(bytearray(buf))
    sound.play()
    time.sleep(duration)  # Duration of the note

# Main function to play the scale
def play_scale(root_freq, strum_speed=0.1):
    scale = generate_major_scale(root_freq)
    for freq in scale:
        play_frequency(freq)
        time.sleep(strum_speed)  # Delay between notes to simulate strumming

# Loop to continuously play the scale
try:
    while True:
        play_scale(440)  # A4 as the root frequency
except KeyboardInterrupt:
    print("Scale loop terminated.")
    pygame.mixer.quit()
