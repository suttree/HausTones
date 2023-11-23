from musical.theory import Note, Scale, Chord
from musical.audio import playback

from timeline import Hit, Timeline

import pprint, random, math
pp = pprint.PrettyPrinter(indent=4)

# .plan
# 15 descending notes
# Every fourth repetition add in a chord with a few seconds of reverb

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
timeline = Timeline()

x = 0.0             # sin/cos variance
interval = 1.3417   # gap between notes
offset = 1.72       # offset applied each loop
iterations = 54     # number of times to loop
amplitude = 2.9     # Amplitude of the oscillation (controls the range)
frequency = 0.9     # Frequency of the oscillation (controls how fast it changes)

def notes_from_scale(starting_note, intervals):
    pp.pprint(starting_note[0])
    starting_note = starting_note[0]
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
scales = ['major', 'pentatonicmajor', 'augmented', 'diminished', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']
s = random.choice(scales)
scale = Scale(key, s)
notes = notes_from_scale(key.note, scale.intervals)
progression = Chord.progression(scale, base_octave=key.octave)

pp.pprint(s)
pp.pprint(scale)
pp.pprint(key)
pp.pprint(notes)

notes = notes[::-1]         # descending
#random.shuffle(notes)       # random

for i in range(iterations):
    for note in notes:
        note = Note(note)

        # main melody
        if(i < 5):
            timeline.add(time + interval, Hit(note, 6.0))
        else:
            timeline.add(time + interval, Hit(note, 6.0))
            timeline.add(time + interval * 2.0, Hit(note.shift_down_octave(1), 4.0))

            if( i < (iterations - 1)):
                timeline.add(time + interval, Hit(note.shift_down_octave(-1), 4.0))

        time += 0.35

        # offset melody
        if( i < 3):
            timeline.add(time + interval, Hit(note, 5.0))
        elif( i < (iterations - 4)):
            timeline.add(time + interval + offset, Hit(note, 3.0))

        time += 0.74

    modulation = amplitude * math.sin(frequency * i)
    x += modulation
    pp.pprint(x)
    
    if( i % 2 == 0 and i > 0):
        interval += x
        offset += x * 0.25

    if( i % 3 == 0 and i > 0):
        timeline.add(time + interval, Hit(note.shift_down_octave(1), 8.0))
        timeline.add(time + interval, Hit(note.shift_down_octave(1), 8.0))
        timeline.add(time + interval, Hit(note.shift_down_octave(2), 8.0))

print("Rendering audio...")
data = timeline.render()

# Reduce volume to 25%
data = data * 0.25

print("Playing audio...")
playback.play(data)