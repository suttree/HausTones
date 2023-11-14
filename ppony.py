from musical.theory import Note, Scale, Chord
from musical.audio import source, effect, playback

from timeline import Hit, Timeline

import numpy, random, pprint, noise

pp = pprint.PrettyPrinter(indent=4)

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([1,2,3,3,4,4,4,5]))).note
key = Note(key_note + '4')

scales = ['major', 'minor', 'melodicminor', 'harmonicminor', 'pentatonicmajor', 'bluesmajor', 'pentatonicminor', 'bluesminor', 'augmented', 'diminished', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']
random.shuffle(scales)
scale = Scale(key, 'chromatic')

print(key)
print(scale)

# Grab progression chords from scale starting at the octave of our key
progression = Chord.progression(scale, base_octave=key.octave)
print(progression)


time = 0.0 # Keep track of correct note placement time in seconds

timeline = Timeline()

note = key
chunks = []

interval = 0.2
offset = 0.8
for i in range(len(progression)):
    for n in range(len(progression[i].notes)):
        third = scale.transpose(note, 2)
        fifth = scale.transpose(key, 4)

        chunks.append(source.sawtooth(third, offset) + source.sawtooth(third, offset))
        chunks.append(source.sine(note, interval) + source.square(note, interval))
        chunks.append(source.pluck(fifth, offset * 2) + source.pluck(fifth, offset * 2))
        note = progression[i].notes[n]
    
#for i in range(len(scale)):
    #note = progression[0].notes[0]
    #third = scale.transpose(note, 2)
    #chunks.append(source.sine(note, 0.7) + source.square(third, 0.7))
    #note = scale.transpose(note, 1)

fifth = scale.transpose(key, 4)
chunks.append(source.sine(key, 1.5) + source.square(fifth, 1.5))

data = numpy.concatenate(chunks)

# Reduce volume to 50%
data = data * 0.5

playback.play(data)