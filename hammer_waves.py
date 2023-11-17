from musical.theory import Note, Scale, Chord
from musical.audio import playback

from timeline import Hit, Timeline

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# .plan
# 15 descinding notes
# Every fourth repetition add in a chord with a few seconds of reverb

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
timeline = Timeline()

interval = 0.2
offset = 0.3

root_note = 'C'
iterations = 10

def notes_from_scale(starting_note, intervals):
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

key = Note(root_note)
scale = Scale(key, 'chromatic')
notes = notes_from_scale(root_note, scale.intervals)
progression = Chord.progression(scale, base_octave=0)

pp.pprint(scale)
pp.pprint(key)
pp.pprint(notes)

for i in range(iterations):
    for note in notes[::-1]:
        timeline.add(time + interval, Hit(Note(note), 4.0))

        if( i == 0):
            timeline.add(time + interval, Hit(Note(note), 4.0))
        elif( i < (iterations - 1)):
            timeline.add(time + interval + offset, Hit(Note(note), 4.0))

        time += 0.7

    if( i % 2 == 0):
        interval += 0.1
        offset += 0.2

    if( i % 3 == 0):
        #chord = progression[0]
        timeline.add(time + interval, Hit(Note(note), 4.0))
        timeline.add(time + interval + 0.1, Hit(Note(note), 5.0))
        timeline.add(time + interval + 0.2, Hit(Note(note), 6.0))
        timeline.add(time + interval + 0.3, Hit(Note(note), 7.0))


    # Strum out root chord to finish
    #chord = progression[0]
    #timeline.add(time + interval, Hit(chord.notes[0], 2.0))
    #timeline.add(time + interval, Hit(chord.notes[0], 2.0))
    #timeline.add(time + interval, Hit(chord.notes[0], 2.0))
"""
all_notes = []
for chord in progression:
    all_notes.append(chord.notes[0])
    all_notes.append(chord.notes[1])
    all_notes.append(chord.notes[2])
pp.pprint(all_notes)
"""

"""
for interval in scale.intervals[::-1]:
    pp.pprint(interval)
    note = scale.transpose(key, interval)
    #progression.root.transpose(interval)
    timeline.add(time + interval, Hit(note, 1.0))
    time += 1.0
"""

"""
for index, note in enumerate(all_notes):
    pp.pprint(note)
    timeline.add(time + interval * index, Hit(note, 0.1))
    time += 0.2
"""

"""
for index in [5, 4, 3, 2, 1, 0]:
    chord = progression[index]
    root, third, fifth = chord.notes
    arpeggio = [fifth, third, root]
    for i, interval in enumerate(arpeggio):
        ts = float(i * 2) / len(arpeggio)
        timeline.add(time + ts, Hit(interval, 1.0))
    time += 2.0
"""

print("Rendering audio...")
data = timeline.render()

# Reduce volume to 25%
data = data * 0.25

print("Playing audio...")
playback.play(data)