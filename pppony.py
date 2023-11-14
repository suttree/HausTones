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


# Just strum notes from the chord
# vary the interval/offset after each n loops
for i in range(len(progression)):
    for n in range(len(progression[i].notes)):
        chord = progression[i]
        timeline.add(time + 0.0, Hit(chord.notes[0], 4.0))
        timeline.add(time + interval, Hit(chord.notes[1], 4.0))
        timeline.add(time + interval * 2, Hit(chord.notes[2], 4.0))
        timeline.add(time + interval * 3, Hit(chord.notes[1].transpose(12), 4.0))
        timeline.add(time + interval * 4, Hit(chord.notes[2].transpose(12), 4.0))
        timeline.add(time + interval * 5, Hit(chord.notes[0].transpose(12), 4.0))

        chord = progression[-i]
        timeline.add(time + 0.0, Hit(chord.notes[0], 4.0))
        timeline.add(time + offset, Hit(chord.notes[1], 4.0))
        timeline.add(time + offset * 2, Hit(chord.notes[2], 4.0))
        timeline.add(time + offset * 3, Hit(chord.notes[1].transpose(12), 4.0))
        timeline.add(time + offset * 4, Hit(chord.notes[2].transpose(12), 4.0))
        timeline.add(time + offset * 5, Hit(chord.notes[0].transpose(12), 4.0))

data = timeline.render()

playback.play(data)