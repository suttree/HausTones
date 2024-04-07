import random

def notes_from_scale(starting_note, intervals):
    starting_note = starting_note[0].upper()
    
    # Define the order of notes in the musical alphabet
    musical_alphabet = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Initialize a list to store the notes
    scale = []
    
    # Find the index of the starting note in the musical alphabet
    current_note_index = musical_alphabet.index(starting_note)
    
    # Append the starting note to the scale
    scale.append(starting_note)
    
    for interval in intervals[:-1]:  # Exclude the last interval
        # Calculate the next note index by adding the interval to the current note index
        next_note_index = (current_note_index + interval) % 12
        next_note = musical_alphabet[next_note_index]
        
        # Append the next note to the scale
        scale.append(next_note)
        
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