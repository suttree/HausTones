from musical.theory import Note, Scale, Chord
from musical.audio import playback
from musical.utils import notes_from_scale

from timeline import Hit, Timeline

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
timeline = Timeline()

interval = 0.2
interval = random.uniform(0.2, 0.6)
offset = 0.3
offset = interval + random.uniform(0.1, 0.8)

iterations = 14
iterations = random.randint(6, 24)

# Define key and scale
key = Note(random.choice(Note.NOTES))
#pp.pprint(key)
scales = ['major', 'pentatonicmajor', 'augmented', 'diminished', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']

scale = Scale(key, random.choice(scales))
notes = notes_from_scale(key.note, scale.intervals)
progression = Chord.progression(scale, base_octave=key.octave)

#pp.pprint(scale)
#pp.pprint(key)
#pp.pprint(notes)

looper_x = random.randint(1, 4)
looper_y = random.randint(2, 5)
looper_z = random.randint(1, 3)

# descending/ascending flip
if(random.randint(0, 1) == 1):
    notes = notes[::-1]

for i in range(iterations):
    for note in notes:
        note = Note(note)

        if( i <= looper_x):
            timeline.add(time + interval, Hit(note, 4.0))
        elif(i > looper_x):
            timeline.add(time + interval, Hit(note, 4.0))
            timeline.add(time + interval, Hit(note, 4.0))
            
            if( i < (iterations - 1)):
                timeline.add(time + interval + offset, Hit(note, 4.0))
                timeline.add(time + interval, Hit(note.shift_down_octave(1), 4.0))

        time += offset

        # repeat lower
        #note = note.shift_down_octave(1)
        #timeline.add(time + interval, Hit(note, 4.0))

        if( i < looper_y):
            timeline.add(time + interval, Hit(note, 4.0))
        elif( i < (iterations - 1)):
            timeline.add(time + interval + offset, Hit(note, 4.0))

        time += offset
        
    if( i % looper_y == 0 and i > 0):
        interval += interval/2
        offset += offset/2

    if( i % looper_z == 0 and i > 0):
        
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
        time += offset
        timeline.add(time + interval, Hit(note, 4.0))
        timeline.add(time + interval + 0.2, Hit(note, 4.0))
        timeline.add(time + interval + 0.4, Hit(note.transpose(12), 4.0))
        """
        
print("Rendering audio...")
data = timeline.render()

# Reduce volume to 25%
#data = data * 0.25

print("Playing audio...")
playback.play(data)