from musical.theory import Note, Scale, Chord
from musical.audio import playback

from timeline import Hit, Timeline

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# Define key and scale
key = Note('C')
scale = Scale(key, 'major')
progression = Chord.progression(scale, base_octave=key.octave)
chord = progression[0]

time = 0.0 # Keep track of currect note placement time in seconds

timeline = Timeline()

offset = 1.5
interval = 0.5
notes = [0, 1, 2]

pp.pprint(key)
pp.pprint(scale)
pp.pprint(notes)

offset = 0.6
interval = 0.2
for i in range(8):
    timeline.add(time + interval * 1, Hit(chord.notes[2].transpose(12), 4.0))
    timeline.add(time + interval * 2, Hit(chord.notes[1].transpose(12), 4.0))
    timeline.add(time + interval * 3, Hit(chord.notes[0].transpose(12), 4.0))
    timeline.add(time + interval * 4, Hit(chord.notes[2], 4.0))
    timeline.add(time + interval * 5, Hit(chord.notes[1], 4.0))
    timeline.add(time + interval * 6, Hit(chord.notes[0], 4.0))

    o_interval = interval + offset
    timeline.add(time + o_interval * 1, Hit(chord.notes[0].transpose(0), 4.0))
    timeline.add(time + o_interval * 2, Hit(chord.notes[1].transpose(0), 4.0))
    timeline.add(time + o_interval * 3, Hit(chord.notes[2].transpose(0), 4.0))

    time += 2.2
    interval += 0.03147

print("Rendering audio...")
data = timeline.render()

# Reduce volume to 25%
data = data * 0.25

print("Playing audio...")
playback.play(data)