from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

scales = ['major', 'pentatonicmajor', 'augmented', 'diminished', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
timeline = Timeline()
interval = random.uniform(1.2, 2.6)
offset_i = random.uniform(0.08, 0.137)
iterations = random.randint(6, 22)
duration = random.uniform(6.0, 12.0)

# Define key and scale
key = Note(random.choice(Note.NOTES))
scale = Scale(key, 'chromatic')
progression = Chord.progression(scale)

for i in range(iterations):
    chord = progression[2]
    timeline.add(time + 0.000, Hit(scale.transpose(chord.notes[0], -12), duration))
    timeline.add(time + 0.000, Hit(chord.notes[0], duration))
    timeline.add(time + 0.050, Hit(scale.transpose(chord.notes[1], -12), duration))
    timeline.add(time + 0.075, Hit(chord.notes[1], duration))
    timeline.add(time + 0.100, Hit(scale.transpose(chord.notes[2], 12), duration))
    timeline.add(time + 0.120, Hit(chord.notes[2], duration))
    timeline.add(time + 0.150, Hit(scale.transpose(chord.notes[0], 12), duration))
    timeline.add(time + 0.150, Hit(scale.transpose(chord.notes[2], 12), duration))

    scale = Scale(chord.notes[2], 'mixolydian')
    progression = Chord.progression(scale)

    time += (2.0 * random.randint(2,6))

#print "Rendering audio..."
data = timeline.render()

data = effect.tremolo(data, freq=0.2)

# Reduce volume to 10%
data = data * 0.05

#print "Playing audio..."
playback.play(data)