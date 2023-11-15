from musical.theory import Note, Scale, Chord
from musical.audio import source, playback

from timeline import Hit, Timeline

import pprint, random, numpy
pp = pprint.PrettyPrinter(indent=4)

# Define key and scale
#key = Note('C')
#scale = Scale(key, 'major')

key = Note(random.choice(Note.NOTES))
scales = ['major', 'pentatonicmajor', 'augmented', 'diminished', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']

scale = Scale(key, random.choice(scales))
progression = Chord.progression(scale, base_octave=key.octave)
chord = progression[0].invert_down()

pp.pprint(key)
pp.pprint(scale)

note = key
chunks = []
duration = 0.25

"""
for i in range(2):
    for j in range(3):
        chunks.append(
            source.sine(key, duration) + 
            source.square(
                scale.transpose(key, j)
            , duration)
        )
        note = scale.transpose(note, 1)
"""

for _ in range(2):
    for i, chord in enumerate(progression):
        pp.pprint(chord)
        for j, _note in enumerate(chord):
            pp.pprint(_note)
            chunks.append(
                source.pluck(key, duration) + 
                source.square(
                    scale.transpose(_note, j)
                , duration)
            )

            duration -= 0.00031479 # use a sin wave for this?

            chunks.append(
                source.square(key, duration) + 
                source.pluck(
                    scale.transpose(_note, j)
                , duration)
            )

"""
for _note in scale:
    chunks.append(
        source.sine(key, duration) + 
        source.square(
            scale.transpose(_note, j)
        , duration)
    )
"""

print("Rendering audio...")
data = numpy.concatenate(chunks)

# Reduce volume to 25%
data = data * 0.25

print("Playing audio...")
playback.play(data)