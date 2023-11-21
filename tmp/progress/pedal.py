from musical.theory import Note, Scale, Chord
from musical.audio import source, playback, effect

from timeline import Hit, Timeline

import pprint, random, numpy, time, math
pp = pprint.PrettyPrinter(indent=4)

key = Note(random.choice(Note.NOTES))
scales = ['major', 'pentatonicmajor', 'augmented', 'diminished', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']

scale = Scale(key, random.choice(scales))
progression = Chord.progression(scale, base_octave=key.octave)
chord = progression[0]

dice_roll = random.randint(0, 5)
if(dice_roll < 2):
    chord = chord.major(chord.notes[0])
elif(dice_roll < 4):
    chord = chord.minor(chord.notes[0])
elif(dice_roll < 6):
    chord = chord.augmented(chord.notes[0])
else:
    chord = chord.diminished(chord.notes[0])
root, third, fifth = chord.notes

pp.pprint(key)
pp.pprint(scale)
pp.pprint(chord.notes)

note = key
chunks = []
duration = 0.25
interval = 0.15
offset = 0.139

for i in range(2):
    for j in range(2):
        pedal = [root, fifth, root, fifth, root, fifth]
        melody = [third, root, third, fifth, third, fifth, third]
        random.shuffle(melody)
        
        for _note in pedal:
            chunks.append(
                source.sine(root.shift_down_octave(0), interval) + 
                source.square(_note.shift_down_octave(2), interval)
            )

        for _note in melody:
            d = offset + math.cos(time.time()) * 0.5
            chunks.append(
                source.sine(root.transpose(-2), d) +
                source.square(_note, d)
            )

            chunks.append(
                source.sine(root, offset) + 
                source.sawtooth(_note.transpose(2), offset)
            )

        #duration += math.cos(time.time()) * 0.10

"""
    for i, chord in enumerate(progression):
        pp.pprint(chord)
        for j, _note in enumerate(chord):
            pp.pprint(_note)
            chunks.append(
                source.sine(key, duration) + 
                source.square(note, duration)
            )
"""



print("Rendering audio...")
data = numpy.concatenate(chunks)
data = effect.tremolo(data, 0.4)
data = effect.flanger(data, 0.1)

# Reduce volume to 25%
data = data * 0.25

print("Playing audio...")
playback.play(data)