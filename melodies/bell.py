# Pick a chord
# Pick a scale
# Pluck/strum the notes of the scale
# Repeat
# Then fuck with intervals etc


# play sequence of notes at interval 0.2
# play harmony notes at interval 0.4
# play chord at end of harmony
# repeat


from musical.theory import Note, Scale, Chord
from musical.audio import source, effect, playback

from timeline import Hit, Timeline

import numpy, random, pprint, noise, math, time

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

iterations = random.randint(2, 8)
interval = 16.0
interval = random.uniform(14.2, 22.8)
offset = 0.6
offset = random.uniform(0.025, 1.2)
pp.pprint(iterations)
pp.pprint(interval)
pp.pprint(offset)
pp.pprint('--setup--')

chord = progression[0]
for i in range(iterations):
    timeline.add(mtime, Hit(chord.notes[0].shift_down_octave(1), interval))
    note = scale.transpose(chord.notes[0].shift_down_octave(1), random.choice((-2, -1, 1, 2)))
    timeline.add(mtime, Hit(note, interval))

    timeline.add(mtime, Hit(chord.notes[1].shift_down_octave(1), interval + offset))
    timeline.add(mtime, Hit(chord.notes[2].shift_down_octave(2), interval + offset))

    mtime += interval - offset

    if(i % 4 == 0 and i > 0):
        mtime -= offset
        interval += 0.1 * math.cos(time.time())
        offset += 0.1 * math.cos(time.time())
        
    if(i % 6 == 0 and i > 0):
        chord = progression[2]

data = timeline.render()
data = effect.feedback_modulated_delay(data, data, 0.36, 0.64)
data = effect.modulated_delay(data, data, 0.2, 1.6)
data = effect.flanger(data, 0.4)

playback.play(data)