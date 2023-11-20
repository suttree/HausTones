# Define the starting note of the scale
starting_note = "C"

# Define the intervals for a major scale
intervals = [2, 2, 1, 2, 2, 2, 1]

# Initialize a list to store the notes
scale = [starting_note]

# Calculate the notes in the scale
current_note = starting_note
for interval in intervals:
    # Calculate the next note by adding the interval to the current note
    next_note_index = (ord(current_note) - ord('A') + interval) % 7
    next_note = chr(ord('A') + next_note_index)
    
    # Append the next note to the scale
    scale.append(next_note)
    
    # Update the current note for the next iteration
    current_note = next_note

print(scale)
