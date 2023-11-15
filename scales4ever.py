from musical.theory import Note, Scale, Chord
from musical.audio import playback

from timeline import Hit, Timeline

import pprint, random
pp = pprint.PrettyPrinter(indent=4)


# TODO
# add in more notes?
    # for j, _note in enumerate(chord):
# sin/cos on the duration and offset wobbles?



# Define key and scale
#key = Note('C')
#scale = Scale(key, 'major')

key = Note(random.choice(Note.NOTES))
scales = ['major', 'pentatonicmajor', 'augmented', 'diminished', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']

scale = Scale(key, random.choice(scales))
progression = Chord.progression(scale, base_octave=key.octave)
chord = progression[0].invert_down()

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
for i in range(80):
    timeline.add(time + interval * 1, Hit(chord.notes[2].transpose(0), 8.0))
    timeline.add(time + interval * 2, Hit(chord.notes[1].transpose(0), 8.0))
    timeline.add(time + interval * 3, Hit(chord.notes[0].transpose(0), 8.0))
    timeline.add(time + interval * 4, Hit(chord.notes[2], 8.0))
    timeline.add(time + interval * 5, Hit(chord.notes[1], 8.0))
    timeline.add(time + interval * 6, Hit(chord.notes[0], 8.0))

    o_interval = interval + offset
    timeline.add(time + o_interval * 1, Hit(chord.notes[0].transpose(0), 8.0))
    timeline.add(time + o_interval * 2, Hit(chord.notes[1].transpose(0), 8.0))
    timeline.add(time + o_interval * 3, Hit(chord.notes[2].transpose(0), 8.0))

    time += 2.2
    interval += 0.025

    if(i % 10 == 0 and i > 0):
        scale = Scale(key, random.choice(scales))
        progression = Chord.progression(scale, base_octave=key.octave)
        chord = progression[0]

    if(i % 20 == 0 and i > 0):
        timeline.add(time + 0.03, Hit(chord.notes[0].transpose(0), 4.0))
        timeline.add(time + 0.04, Hit(chord.notes[1].transpose(-6), 4.0))
        timeline.add(time + 0.05, Hit(chord.notes[2].transpose(-12), 4.0))
        time += 4.0

print("Rendering audio...")
data = timeline.render()

# Reduce volume to 25%
data = data * 0.25

print("Playing audio...")
playback.play(data)