import random,os
from datetime import datetime
import soundfile as sf
import numpy as np
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def compress_audio(audio, threshold=-20, ratio=3, attack=5, release=50):
    # Convert threshold to linear scale
    threshold_linear = 10 ** (threshold / 20)
    
    # Apply compression
    compressed_audio = np.zeros_like(audio)
    gain = 1.0
    for i in range(len(audio)):
        if np.abs(audio[i]) > threshold_linear:
            gain = threshold_linear / (ratio * np.abs(audio[i]))
        else:
            gain = 1.0
        gain = max(gain, compressed_audio[i-1] * np.exp(-1 / (release * 44100)))
        gain = min(gain, compressed_audio[i-1] * np.exp(1 / (attack * 44100)))
        compressed_audio[i] = audio[i] * gain
    
    return compressed_audio

def save_normalized_audio(data, samplerate=44100, current_script_filename='utils.py'):
    # Save the rendered audio to a temporary file
    temp_file = "output/temp_audio.wav"
    sf.write(temp_file, data, samplerate=samplerate)

    # Load the audio file with soundfile
    audio, sr = sf.read(temp_file)

    # Apply bandpass filter to limit extreme frequencies
    lowcut = 100 # Hz
    highcut = 10000 # Hz
    filtered_audio = butter_bandpass_filter(audio, lowcut, highcut, sr)

    # Apply audio compression
    compressed_audio = compress_audio(filtered_audio)

    # Normalize the audio
    max_val = np.max(np.abs(compressed_audio))
    epsilon = 1e-8  # Small value to avoid division by zero

    if max_val < 1e-6:
        print("Warning: Audio signal is very weak. Skipping normalization.")
        normalized_audio = compressed_audio
    else:
        normalized_audio = compressed_audio / (max_val + epsilon)

    # Generate the output file name with the script name and timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output/{current_script_filename}_output_{timestamp}.wav"

    # Save the normalized audio to the output file
    sf.write(output_file, normalized_audio, samplerate=sr)

    print(f"Audio exported as {output_file}")
    return output_file
    
def notes_from_scale(starting_note, intervals, octave=4):
    starting_note = starting_note[0].upper()
    
    # Define the order of notes in the musical alphabet
    musical_alphabet = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Initialize a list to store the notes
    scale = []
    
    # Find the index of the starting note in the musical alphabet
    current_note_index = musical_alphabet.index(starting_note)
    
    # Append the starting note to the scale with the specified octave
    scale.append(starting_note + str(octave))
    
    for interval in intervals[:-1]:  # Exclude the last interval
        # Calculate the next note index by adding the interval to the current note index
        next_note_index = (current_note_index + interval) % 12
        
        # Determine the octave of the next note
        if next_note_index < current_note_index:
            octave += 1
        
        next_note = musical_alphabet[next_note_index]
        
        # Append the next note to the scale with the appropriate octave
        scale.append(next_note + str(octave))
        
        # Update the current note index for the next iteration
        current_note_index = next_note_index
    
    return scale

def extended_notes_from_scale(starting_note, intervals, num_octaves=2, default_octave=3):
    # Define the order of notes in the musical alphabet
    musical_alphabet = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Initialize a list to store the notes
    scale = []
    
    # Extract the note name and octave number from the starting note
    note_name = starting_note[:-1].upper() if starting_note[-1].isdigit() else starting_note.upper()
    octave = int(starting_note[-1]) if starting_note[-1].isdigit() else default_octave
    
    # Find the index of the starting note in the musical alphabet
    current_note_index = musical_alphabet.index(note_name)
    
    for _ in range(num_octaves):
        for interval in intervals:
            # Append the current note to the scale with the appropriate octave
            scale.append(musical_alphabet[current_note_index] + str(octave))
            
            # Calculate the next note index by adding the interval to the current note index
            next_note_index = (current_note_index + interval) % 12
            
            # Increment the octave if the next note crosses the octave boundary
            if next_note_index < current_note_index:
                octave += 1
            
            # Update the current note index for the next iteration
            current_note_index = next_note_index
    
    return scale

def add_intervals_to_notes(notes):
    notes_with_intervals = []
    interval = 0.0
    
    for note in notes:
        notes_with_intervals.append([note, add_random_float(interval, -0.8, 1.02)])
        interval += 1.2

    return notes_with_intervals
    
def add_random_float(value, min_val=0.0, max_val=1.0):
    random_float = random.uniform(min_val, max_val)
    return round(value + random_float, 2)