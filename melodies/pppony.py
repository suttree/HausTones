from musical.theory import Note, Scale, Chord
from musical.audio import source, effect, playback

from timeline import Hit, Timeline

import numpy, random, pprint, math, time

pp = pprint.PrettyPrinter(indent=4)

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([1,1,2,2,3,3,4]))).note
key = Note(key_note + '4')

scales = ['pentatonicmajor', 'mixolydian', 'phrygian', 'japanese', 'pentatonicminor', 'pentatonicmajor']
random.shuffle(scales)
scale = Scale(key, scales[0])

print(key)
print(scale)

# Grab progression chords from scale starting at the octave of our key
progression = Chord.progression(scale, base_octave=key.octave)
print(progression)

mtime = 0.0 # Keep track of correct note placement time in seconds

timeline = Timeline()

note = key
chunks = []

iterations = random.randint(8, 48)
interval = random.uniform(0.2, 1.4) #0.4
offset = random.uniform(0.3, 0.9) #0.6

for i in range(iterations):
    if (i > iterations - 4): break # skip the lone notes at the end
    
    for j in range(len(progression)):
        for n in range(len(progression[j].notes)):
            chord = progression[j]
            timeline.add(mtime + 0.0, Hit(chord.notes[0], 4.2))
            timeline.add(mtime + interval, Hit(chord.notes[1], 4.0))
            timeline.add(mtime + interval * 2, Hit(chord.notes[2], 4.2))

            chord = progression[0]
            timeline.add(mtime + 0.0, Hit(chord.notes[0], 3.2))
            timeline.add(mtime + offset, Hit(chord.notes[1], 3.8))
            timeline.add(mtime + offset * 2.2, Hit(chord.notes[2], 4.2))

        mtime += interval + offset

        if(i % 40 == 0 and i > 0):
            mtime -= random.uniform(-0.02, 0.4) #0.026

        if(i % 22 == 0 and i > 0):
            interval += 0.04 * math.cos(time.time())
            offset += 0.06 * math.cos(time.time())

data = timeline.render()
#data = effect.feedback_modulated_delay(data, data, 0.0036, 0.0064)
data = effect.modulated_delay(data, data, 0.004, 0.26)
#data = effect.tremolo(data, 0.024)
data = effect.shimmer(data, 12.74)

playback.play(data)