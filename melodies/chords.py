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

# Grab progression chords from scale starting at the octave of our key
progression = Chord.progression(scale)
chord = progression[0]

time = 0.0 # Keep track of currect note placement time in seconds
interval = random.uniform(0.8, 2.8)
offset = 0.0
iterations = random.randint(4, 10)
duration = random.uniform(1.0, 8.0)

timeline = Timeline()

for i in range(iterations):
    # simple/dumb way of creating a chord progression
    notes = [0,0,1,1,2,3,3]
    chord_progression = []
    for i in range(2):
        random.shuffle(notes)
        for note in notes:
            chord_progression.append(note)

    for index in chord_progression:
        offset = random.uniform(0.07, 2.625)

        chord = progression[index]
        #if(i == random.randint(0,2)):
        #    chord = chord.diminished(chord.notes[0])
        #elif(i == random.randint(iterations - 2, iterations)):
        #    chord = chord.augmented(chord.notes[0])
        #root, third, fifth = chord.notes

        timeline.add(time + 0.00 + offset, Hit(chord.notes[0].transpose(-2), duration))
        timeline.add(time + 0.00 + offset, Hit(chord.notes[2].transpose(-2), duration))
        
        timeline.add(time + 0.01 + offset, Hit(chord.notes[0], duration))
        timeline.add(time + 0.02 + offset, Hit(chord.notes[2], duration))
        timeline.add(time + 0.04 + offset, Hit(chord.notes[2], duration))

        timeline.add(time + 0.06 + offset, Hit(chord.notes[0].transpose(12), duration))
        timeline.add(time + 0.08 + offset, Hit(chord.notes[2].transpose(12), duration))
        timeline.add(time + 0.10 + offset, Hit(chord.notes[2].transpose(12), duration))

        time += interval * random.uniform(1.8, 2.2)

#print "Rendering audio..."
data = timeline.render()

data = effect.tremolo(data, 0.1)
#data = effect.flanger(data, 0.1)

# Reduce volume to 25%
data = data * 0.25

#print "Playing audio..."
playback.play(data)

#print "Done!"
