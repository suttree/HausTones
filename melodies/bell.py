from musical.theory import Note, Scale, Chord
from musical.audio import source, effect, playback

from timeline import Hit, Timeline

import numpy, random, pprint, math, time

pp = pprint.PrettyPrinter(indent=4)

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([1,2,3,4,5]))).note
key = Note(key_note)

scales = ['pentatonicmajor', 'mixolydian', 'phrygian', 'japanese', 'pentatonicminor', 'pentatonicmajor']
random.shuffle(scales)
scale = Scale(key, scales[0])

print(key)
print(scale)

# Grab progression chords from scale starting at the octave of our key
progression = Chord.progression(scale, base_octave=key.octave)
chord = progression[0]
chord = chord.augmented(chord.notes[0])
print(chord)

mtime = 0.0 # Keep track of correct note placement time in seconds

timeline = Timeline()

note = key
chunks = []

iterations = random.randint(5, 12)
interval = random.uniform(14.2, 22.8)
offset = random.uniform(0.025, 1.78)
pp.pprint(iterations)
pp.pprint(interval)
pp.pprint(offset)
pp.pprint('--setup--')

chord = progression[0]
for i in range(iterations):
    timeline.add(mtime, Hit(chord.notes[0].shift_down_octave(1), interval))
    note = scale.transpose(chord.notes[0].shift_down_octave(1), random.choice((-2, -1, 1, 2)))
    timeline.add(mtime, Hit(note, interval))

    mtime += 0.02
    timeline.add(mtime, Hit(chord.notes[1].shift_down_octave(1), interval + offset))
    timeline.add(mtime, Hit(chord.notes[2].shift_down_octave(2), interval + offset))
    mtime -= 0.04

    mtime += interval - offset

    if(i % 2 == 0 and i > 0):
        mtime -= offset
        interval -= 0.042 * math.cos(time.time())
        offset -= 0.04 * math.cos(time.time())

    if(i % 3 == 0 and i > 0):
        chord = progression[2]
        
    if(i % 5 == 0 and i > 0):
        mtime -= offset
        interval -= 0.037 * math.cos(time.time())
        offset -= 0.036 * math.cos(time.time())

    if(i % 7 == 0 and i > 0):
        chord = progression[1]

    # add some more overlap:
    if(i % 8 == 0 and i > 0):
        mtime -= 4.25

    if(i % 9 == 0 and i > 0):
        chord = progression[0]

data = timeline.render()
#data = effect.shimmer(data, 3.147)
data = effect.feedback_modulated_delay(data, data, 0.36, 0.84)
#data = effect.modulated_delay(data, data, 0.2, 1.6)
#data = effect.flanger(data, 0.4)
data = effect.reverb(data, 0.8, 0.025)

playback.play(data)