from musical.theory import Note, Scale, Chord
from musical.audio import playback, effect

from timeline import Hit, Timeline

import pprint, random, math
pp = pprint.PrettyPrinter(indent=4)

# .plan
# 15 descending notes
# Every fourth repetition add in a chord with a few seconds of reverb

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
timeline = Timeline()

interval = 0.1      # gap between notes
offset = 0.2        # offset applied each loop
iterations = 12     # number of times to loop

def notes_from_scale(starting_note, intervals):
    pp.pprint(starting_note[0])
    starting_note = starting_note[0].upper()
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

    return scale

# Define key and scale
key = Note(random.choice(Note.NOTES))
scale = Scale(key, 'chromatic')
notes = notes_from_scale(key.note, scale.intervals)
progression = Chord.progression(scale, base_octave=key.octave)

pp.pprint('chromatic..')
pp.pprint(scale)
pp.pprint(key)
pp.pprint(notes)

#notes = notes[::-1]         # descending
#random.shuffle(notes)       # random

for i in range(iterations):
    base_time = time
    for note in notes:
        note = Note(note)

        # main melody
        timeline.add(time, Hit(note, 3.14))
        time += interval
        
    time = base_time
    for note in notes:
        note = Note(note)

        # main melody
        timeline.add(time, Hit(note, 3.14*2))
        time += offset
        
    time = base_time
    for note in notes:
        note = Note(note)

        # main melody
        timeline.add(time, Hit(note, 3.14))
        time += interval + offset
        
    if( i % 3 == 0 and i > 0):
        timeline.add(time + interval, Hit(note.shift_down_octave(1), 8.0))
        timeline.add(time + interval, Hit(note.shift_down_octave(1), 8.0))
        timeline.add(time + interval, Hit(note.shift_down_octave(2), 8.0))
        
    if( i % 6 == 0 and i > 0):
        timeline.add(time + 0.1, Hit(note.shift_down_octave(1), 8.0))
        timeline.add(time + 0.2, Hit(note.shift_down_octave(1), 8.0))
        timeline.add(time + 0.3, Hit(note.shift_down_octave(2), 8.0))


print("Rendering audio...")
data = timeline.render()

# Reduce volume to 25%
data = data * 0.25
data = effect.tremolo(data, 0.3)
#data = effect.flanger(data, 0.4)

print("Playing audio...")
playback.play(data)