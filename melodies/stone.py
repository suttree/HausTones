from musical.theory import Note, Scale, Chord
from musical.audio import playback
from musical.utils import notes_from_scale

from timeline import Hit, Timeline

import pprint, random, math
pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
timeline = Timeline()

x = 0.0             # sin/cos variance
interval = 1.3417   # gap between notes
offset = 1.72       # offset applied each loop
iterations = 12     # number of times to loop
amplitude = 2.9     # Amplitude of the oscillation (controls the range)
frequency = 0.9     # Frequency of the oscillation (controls how fast it changes)

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
        timeline.add(time + interval, Hit(note, 6.0))
        timeline.add(time + interval * 2.0, Hit(note.shift_down_octave(1), 4.0))

        if( i < (iterations - 1)):
            timeline.add(time + interval, Hit(note.shift_down_octave(-1), 4.0))

        time += 0.35

        # offset melody
        if( i < 2):
            timeline.add(time + interval, Hit(note, 5.0))
        elif( i < (iterations - 2)):
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