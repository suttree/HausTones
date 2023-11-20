from musical.theory import Note, Scale, Chord
from musical.audio import source, playback, effect

from timeline import Hit, Timeline

import pprint, random, numpy, time, math
pp = pprint.PrettyPrinter(indent=4)

# Define key and scale
#key = Note('C')
#scale = Scale(key, 'major')

key = Note(random.choice(Note.NOTES))
scales = ['major', 'pentatonicmajor', 'augmented', 'diminished', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']

scale = Scale(key, random.choice(scales))
progression = Chord.progression(scale, base_octave=key.octave)
chord = progression[0]
#chord = chord.diminished(chord.notes[0])
chord = chord.augmented(chord.notes[0])
root, third, fifth = chord.notes

pp.pprint(key)
pp.pprint(scale)
pp.pprint(chord.notes)

note = key
chunks = []
duration = 0.125
interval = 0.0125
offset = 0.127

for i in range(4):
    for j in range(2):
        #varb = duration
        #varb = duration + (1 - math.cos(time.time()))
        #duration = min(max(duration, 0.1), 6.0)

        arpeggio = [root, third, fifth, root, third, fifth]
        random.shuffle(arpeggio)
        
        for _note in arpeggio:            
            chunks.append(
                source.sine(root, duration) + 
                source.square(_note, duration)
            )

            chunks.append(
                source.sine(root, offset) + 
                source.sawtooth(_note.transpose(12), offset)
            )
            
            #pp.pprint(varb)
            #pp.pprint(duration)
            
            #duration = varb
            #pp.pprint(duration)
            #pp.pprint('----')
            
        #duration += 0.31479

    if(i % 2 == 0):
        duration -= interval
    else:
        duration + (1 - math.cos(time.time()))

    """
    for _note in scale:
        chunks.append(
            source.sine(root.octave, duration) + 
            source.square(_note.octave, duration)
        )
    """


"""
for _ in range(2):
    for i, chord in enumerate(progression):
        pp.pprint(chord)
        for j, _note in enumerate(chord):
            pp.pprint(_note)
            chunks.append(
                source.sine(key, duration) + 
                source.square(note, duration)
            )

            #duration -= 0.00031479 # use a sin wave for this?
            duration += duration * varb

            chunks.append(
                source.square(key, duration) + 
                source.sine(_note, duration)
            )

            duration += 0.31479

            for _note in scale:
                chunks.append(
                    source.sine(key, duration) + 
                    source.square(_note, duration)
                )
"""



print("Rendering audio...")
data = numpy.concatenate(chunks)
data = effect.tremolo(data, 0.3)
data = effect.flanger(data, 0.4)

# Reduce volume to 25%
data = data * 0.25

print("Playing audio...")
playback.play(data)