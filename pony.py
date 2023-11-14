from musical.theory import Note, Scale, Chord
from musical.audio import source, effect, playback

from timeline import Hit, Timeline

import numpy, random

# Define key and scale
key = Note((random.choice(Note.NOTES), random.choice([2,3,3])))

key = Note('D4')

key_note = Note((random.choice(Note.NOTES), random.choice([2,3,3]))).note
key = Note(key_note + '4')

scales = ['major', 'minor', 'melodicminor', 'harmonicminor', 'pentatonicmajor', 'bluesmajor', 'pentatonicminor', 'bluesminor', 'augmented', 'diminished', 'wholehalf', 'halfwhole', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']
random.shuffle(scales)
scale = Scale(key, random.choice(scales))

print(key)
print(scale)

# Grab progression chords from scale starting at the octave of our key
progression = Chord.progression(scale, base_octave=key.octave)

time = 0.0 # Keep track of correct note placement time in seconds

timeline = Timeline()

# Pick a notes from a chord randomly chosen from a list of notes in this progression
chord = progression[ random.choice(range(len(progression)-1)) ]
notes = chord.notes

# Testing a new melody-generation idea - duncan 11/4/20
# - needs more work, disabling for now - 12/4/20
random_melody = []
melody_length = random.randrange(12, 24)

for i in range(0, melody_length):
    random_melody.append( round(random.uniform(0.6, 2.4), 1) )
print(random_melody)

for i, interval in enumerate(random_melody):
    random_note = random.choice(notes)
    #note = random_note.transpose(0)
    note = random_note

    time = time + interval
    timeline.add(time, Hit(note.transpose(-12), interval))
    timeline.add(time, Hit(note, interval))
    timeline.add(time, Hit(note.transpose(12), interval))

# Add progression to timeline by arpeggiating chords from the progression
for index in [0, 2, 3, 1,    0, 2, 3, 4,    5, 4, 0]:
    chord = progression[index]
    root, third, fifth = chord.notes
    arpeggio = [root, third, fifth, third, root, third, fifth, third]
    for i, interval in enumerate(arpeggio):
        ts = float(i * 2) / len(arpeggio)
        timeline.add(time + ts, Hit(interval, 1.0))
    time += 2.0

chord = progression[0]
timeline.add(time + 0.0, Hit(chord.notes[0], 4.0))
timeline.add(time + 0.1, Hit(chord.notes[1], 4.0))
timeline.add(time + 0.2, Hit(chord.notes[2], 4.0))
timeline.add(time + 0.3, Hit(chord.notes[1].transpose(12), 4.0))
timeline.add(time + 0.4, Hit(chord.notes[2].transpose(12), 4.0))
timeline.add(time + 0.5, Hit(chord.notes[0].transpose(12), 4.0))

data = timeline.render()
data = effect.chorus(data, freq=3.14159)
playback.play(data)

note = key
chunks = []
for i in range(len(scale)):
    third = scale.transpose(note, 2)
    chunks.append(source.sine(note, 0.5) + source.square(third, 0.5))
    note = scale.transpose(note, 1)
fifth = scale.transpose(key, 4)
chunks.append(source.sine(key, 1.5) + source.square(fifth, 1.5))

data = numpy.concatenate(chunks)

# Reduce volume to 50%
data = data * 0.5

playback.play(data)