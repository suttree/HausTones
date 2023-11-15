from musical.theory import Note, Scale, Chord
from musical.audio import playback

from timeline import Hit, Timeline

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# Define key and scale
#key = Note('C')
#scale = Scale(key, 'major')

key = Note(random.choice(Note.NOTES))
scales = ['major', 'minor', 'melodicminor', 'harmonicminor', 'pentatonicmajor', 'bluesmajor', 'pentatonicminor', 'bluesminor', 'augmented', 'diminished', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']
scale = Scale(key, random.choice(scales))


# Grab progression chords from scale starting at the octave of our key
progression = Chord.progression(scale, base_octave=key.octave)

time = 0.0 # Keep track of currect note placement time in seconds

timeline = Timeline()



for index in range(4):
    chord = progression[index]
    timeline.add(time + 0.0, Hit(chord.notes[0], 4.0))
    timeline.add(time + 0.1, Hit(chord.notes[1], 4.0))
    timeline.add(time + 0.2, Hit(chord.notes[2], 4.0))
    timeline.add(time + 0.3, Hit(chord.notes[1].transpose(12), 4.0))
    timeline.add(time + 0.4, Hit(chord.notes[2].transpose(12), 4.0))
    timeline.add(time + 0.5, Hit(chord.notes[0].transpose(12), 4.0))
    time += 2.0

for index in range(4):
    chord = progression[index]
    timeline.add(time + 0.0, Hit(chord.notes[0], 4.0))
    timeline.add(time + 0.01, Hit(chord.notes[1], 4.0))
    timeline.add(time + 0.02, Hit(chord.notes[2], 4.0))
    timeline.add(time + 0.03, Hit(chord.notes[1].transpose(12), 4.0))
    timeline.add(time + 0.04, Hit(chord.notes[2].transpose(12), 4.0))
    timeline.add(time + 0.05, Hit(chord.notes[0].transpose(12), 4.0))
    time += 2.0

for index in range(4):
    chord = progression[index]
    timeline.add(time + 0.0, Hit(chord.notes[0], 4.0))
    timeline.add(time + 0.5, Hit(chord.notes[1], 4.0))
    timeline.add(time + 1.0, Hit(chord.notes[2], 4.0))
    timeline.add(time + 1.5, Hit(chord.notes[1].transpose(12), 4.0))
    timeline.add(time + 2.0, Hit(chord.notes[2].transpose(12), 4.0))
    timeline.add(time + 2.5, Hit(chord.notes[0].transpose(12), 4.0))
    time += 2.0

"""
root = key
second = scale.transpose(root, 1)
third = scale.transpose(root, 2)
fourth = scale.transpose(root, 3)
fifth = scale.transpose(root, 4)
sixth = scale.transpose(root, 5)

# Add progression to timeline by arpeggiating chords from the progression
for index in [1, 3, 5, 0]:
    chord = progression[index]
    #pp.pprint(chord)

    root, third, fifth = chord.notes
    arpeggio = [root, second, third, fourth, fifth, sixth]
    for i, interval in enumerate(arpeggio):
        ts = float(i * 2) / len(arpeggio)
        timeline.add(time + ts, Hit(interval, 2.0))
        time += 0.2

# Strum out root chord to finish
chord = progression[0]
timeline.add(time + 0.0, Hit(chord.notes[0], 4.0))
timeline.add(time + 0.1, Hit(chord.notes[1], 4.0))
timeline.add(time + 0.2, Hit(chord.notes[2], 4.0))
timeline.add(time + 0.3, Hit(chord.notes[1].transpose(12), 4.0))
timeline.add(time + 0.4, Hit(chord.notes[2].transpose(12), 4.0))
timeline.add(time + 0.5, Hit(chord.notes[0].transpose(12), 4.0))
"""

"""
for i in range(4):
    chord = progression[i]
    root, third, fifth = chord.notes

    arpeggio = [root, third, fifth, third, root, third, fifth, third]
    random.shuffle(arpeggio)
    pp.pprint(arpeggio)

    offset = 0.2
    for i, interval in enumerate(arpeggio):
        time = time + (i * offset)
        timeline.add(time, Hit(chord.notes[0], 2.0))
    """

"""
    timeline.add(time + 0.1, Hit(chord.notes[1], 2.0))
    timeline.add(time + 0.2, Hit(chord.notes[2], 2.0))
    timeline.add(time + 0.3, Hit(chord.notes[1].transpose(12), 2.0))
    timeline.add(time + 0.4, Hit(chord.notes[2].transpose(12), 2.0))
    timeline.add(time + 0.5, Hit(chord.notes[0].transpose(12), 2.0))
    timeline.add(time + 0.6, Hit(chord.notes[0].transpose(12), 2.0))
    timeline.add(time + 0.7, Hit(chord.notes[2].transpose(12), 2.0))
    
    chord = progression[2]
    timeline.add(time + 0.0, Hit(chord.notes[0], 2.0))
    timeline.add(time + 0.1, Hit(chord.notes[1], 2.0))
    timeline.add(time + 0.2, Hit(chord.notes[2], 2.0))
    timeline.add(time + 0.3, Hit(chord.notes[1].transpose(12), 2.0))
    timeline.add(time + 0.4, Hit(chord.notes[2].transpose(12), 2.0))
    timeline.add(time + 0.5, Hit(chord.notes[0].transpose(12), 2.0))
    timeline.add(time + 0.6, Hit(chord.notes[0].transpose(12), 2.0))
    timeline.add(time + 0.7, Hit(chord.notes[2].transpose(12), 2.0))
"""

"""
    # Add progression to timeline by arpeggiating chords from the progression
for index in [0, 2, 3, 1,    0, 2, 3, 4,    5, 4, 0]:
    chord = progression[index]
    root, third, fifth = chord.notes
    arpeggio = [root, third, fifth, third, root, third, fifth, third]
    for i, interval in enumerate(arpeggio):
        ts = float(i * 2) / len(arpeggio)
        timeline.add(time + ts, Hit(interval, 1.0))
    time += 2.0
"""

print("Rendering audio...")

data = timeline.render()

# Reduce volume to 25%
data = data * 0.25

print("Playing audio...")

playback.play(data)

print("Done!")
