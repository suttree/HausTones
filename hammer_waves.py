from musical.theory import Note, Scale, Chord
from musical.audio import playback

from timeline import Hit, Timeline

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# .plan
# 15 descending notes
# Every fourth repetition add in a chord with a few seconds of reverb

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
timeline = Timeline()

interval = 0.2
offset = 0.3

root_note = 'F'
iterations = 5

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
#key = Note(root_note)
#scale = Scale(key, 'chromatic')
key = Note(random.choice(Note.NOTES))
pp.pprint(key)
root_note = key.note
scales = ['major', 'pentatonicmajor', 'augmented', 'diminished', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']

scale = Scale(key, random.choice(scales))
notes = notes_from_scale(root_note, scale.intervals)
progression = Chord.progression(scale, base_octave=key.octave)

pp.pprint(scale)
pp.pprint(key)
pp.pprint(notes)

for i in range(iterations):
    for note in notes[::-1]:
        note = Note(note)

        if( i < 2):
            timeline.add(time + interval, Hit(note, 4.0))
        elif(i > 2):
            timeline.add(time + interval, Hit(note, 4.0))
            timeline.add(time + interval, Hit(note, 4.0))
            
            if( i < (iterations - 1)):
                timeline.add(time + interval + offset, Hit(note, 4.0))
                timeline.add(time + interval, Hit(note.shift_down_octave(1), 4.0))

        time += 0.7

        # repeat lower
        #note = note.shift_down_octave(1)
        #timeline.add(time + interval, Hit(note, 4.0))

        if( i < 2):
            timeline.add(time + interval, Hit(note, 4.0))
        elif( i < (iterations - 1)):
            timeline.add(time + interval + offset, Hit(note, 4.0))

        time += 0.7
        
    if( i % 2 == 0 and i > 0):
        interval += 0.15
        offset += 0.25

    if( i % 3 == 0 and i > 0):
        
        """
        chord = progression[0]
        timeline.add(time + 0.3, Hit(chord.notes[2].transpose(12), 4.0))
        timeline.add(time + 0.4, Hit(chord.notes[1].transpose(12), 4.0))
        timeline.add(time + 0.5, Hit(chord.notes[0].transpose(12), 4.0))
        timeline.add(time + 0.0, Hit(chord.notes[2], 4.0))
        timeline.add(time + 0.1, Hit(chord.notes[1], 4.0))
        timeline.add(time + 0.2, Hit(chord.notes[0], 4.0))
        """

        timeline.add(time + interval, Hit(note.shift_down_octave(1), 8.0))
        timeline.add(time + interval, Hit(note.shift_down_octave(1), 8.0))
        timeline.add(time + interval, Hit(note.shift_down_octave(2), 8.0))

        """
        timeline.add(time + interval, Hit(note, 4.0))
        timeline.add(time + interval + 0.1, Hit(note, 4.0))
        timeline.add(time + interval + 0.2, Hit(note, 4.0))
        timeline.add(time + interval + 0.3, Hit(note.transpose(12), 4.0))
        timeline.add(time + interval + 0.4, Hit(note.transpose(12), 4.0))
        timeline.add(time + interval + 0.5, Hit(note.transpose(12), 4.0))
        """
        
print("Rendering audio...")
data = timeline.render()

# Reduce volume to 25%
data = data * 0.25

print("Playing audio...")
playback.play(data)