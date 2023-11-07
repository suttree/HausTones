import numpy as np
import sounddevice as sd
import time
import queue
import threading

# Parameters
scale = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]  # C major scale frequencies (C4 to C5)
fs = 44100  # Sampling rate in Hertz
base_duration = 1.0  # Base duration in seconds for a tone
max_interval = 0.5  # Shorter max interval in seconds between successive tones
tone_queue = queue.Queue()  # Queue to manage tones

# Generate a tone with a specific frequency and duration
def generate_tone(frequency, duration, fs):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    tone = np.sin(2 * np.pi * frequency * t)
    return tone

# Function to play tones from the queue
def play_from_queue():
    while True:
        item = tone_queue.get()  # Block until a tone is available
        if item is None:
            break  # None is the signal to stop
        sd.play(item, samplerate=fs, blocking=False)
        tone_queue.task_done()

# Start the tone player thread
player_thread = threading.Thread(target=play_from_queue)
player_thread.start()

# Function to add a frequency to the queue
def queue_tone(frequency, duration):
    tone = generate_tone(frequency, duration, fs)
    tone *= 32767 / np.max(np.abs(tone))
    tone = tone.astype(np.int16)
    tone_queue.put(tone)

# Start generating and queuing tones
print("Starting wind chime... Press Ctrl+C to stop.")
try:
    next_play_time = time.time() - max_interval  # Start immediately
    while True:
        current_time = time.time()
        if current_time >= next_play_time:
            # Randomly select a frequency from the scale
            frequency = np.random.choice(scale)
            # Randomize duration to vary the sound
            duration = np.random.uniform(0.5, base_duration)
            queue_tone(frequency, duration)
            # Schedule the next tone based on a sine wave interval
            next_play_time += max_interval
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Stopping wind chime...")
finally:
    # Stop the player thread
    tone_queue.put(None)  # Signal to stop the thread
    player_thread.join()
    sd.stop()  # Stop any remaining sound
    print("Wind chime stopped.")
