from musical.theory import Note, Scale, Chord
from musical.audio import playback

from timeline import Hit, Timeline

import pprint, random, keyboard
pp = pprint.PrettyPrinter(indent=4)

# Define key and scale
#key = Note('C')
#scale = Scale(key, 'major')
#progression = Chord.progression(scale, base_octave=key.octave)

key = Note((random.choice(Note.NOTES)))
scales = ['major', 'melodicminor', 'pentatonicmajor', 'augmented', 'diminished', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']
random.shuffle(scales)
scale = Scale(key, random.choice(scales))

# Grab progression chords from scale starting at the octave of our key
progression = Chord.progression(scale, base_octave=key.octave)

chord = progression[ random.choice(range(len(progression)-1)) ]
notes = chord.notes

pp.pprint(chord)
pp.pprint(notes)
pp.pprint('========')
time = 0.0 # Keep track of currect note placement time in seconds

timeline = Timeline()


"""
for index in range(4):
    chord = progression[index]
    timeline.add(time + 0.0, Hit(chord.notes[0], 4.0))
    timeline.add(time + 0.5, Hit(chord.notes[1], 4.0))
    timeline.add(time + 1.0, Hit(chord.notes[2], 4.0))
    timeline.add(time + 1.5, Hit(chord.notes[1].transpose(12), 4.0))
    timeline.add(time + 2.0, Hit(chord.notes[2].transpose(12), 4.0))
    timeline.add(time + 2.5, Hit(chord.notes[0].transpose(12), 4.0))
    time += 3.0
"""

offset = 1.5
interval = 0.5
notes = [0, 1, 2]

for x in range(2):
    pp.pprint(key)
    pp.pprint(scale)
    pp.pprint(notes)
    for index in range(4):
        chord = progression[index]

        for j in range(4):
            note = random.choice(notes)
            timeline.add(time + (interval * j), Hit(chord.notes[note], 3.0))
        time += 3.0
    
    chord = progression[x]
    timeline.add(time + 0.0, Hit(chord.notes[0], 4.0))
    timeline.add(time + 0.01, Hit(chord.notes[1], 4.0))
    timeline.add(time + 0.02, Hit(chord.notes[2], 4.0))
    timeline.add(time + 0.03, Hit(chord.notes[1].transpose(12), 4.0))
    timeline.add(time + 0.04, Hit(chord.notes[2].transpose(12), 4.0))
    timeline.add(time + 0.05, Hit(chord.notes[0].transpose(12), 4.0))
    time += 2.0
    
    scales = ['major', 'melodicminor', 'pentatonicmajor', 'augmented', 'diminished', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']
    scale = Scale(key, random.choice(scales))
    progression = Chord.progression(scale, base_octave=key.octave)

    interval += 0.314


print("Rendering audio...")

data = timeline.render()

# Reduce volume to 25%
data = data * 0.25

print("Playing audio...")

playback.play(data)

print("Done!")
