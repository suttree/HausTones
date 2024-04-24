from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline

from musical.utils import notes_from_scale

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
offset = 0.03479
iterations = random.randint(28, 94)
duration = random.uniform(3.9, 6.2) #4.286
timeline = Timeline()

# Define key and scale
key = Note('F4')
scale = Scale(key, 'chromatic')
progression = Chord.progression(scale)
chord = progression[0]
notes = notes_from_scale(key.note, scale.intervals)

for i in range(iterations):
    if (i > iterations -3): break # skip the lone notes at the end

    for j, note in enumerate(notes[::-1]):
        timeline.add(time + offset * j, Hit(Note(note), duration))
    time += random.uniform(1.02, 1.68) #1.286

    if(offset > 1.2):
        offset -= 0.023
    elif(offset < 0.1):
        offset += 0.022
    else:
        offset += 0.021

    if(i % 11 == 0 and i > 0):
        d_note = chord.diminished(Note(note)).notes[2]
        timeline.add(time + offset, Hit(d_note.shift_up_octave(1), duration * 1.72))

    if(i % 12 == 0 and i > 0):
        timeline.add(time + offset * 1.016, Hit(Note(note).shift_down_octave(0), duration * 1.52))
        timeline.add(time + offset * 1.025, Hit(Note(note).shift_down_octave(1), duration * 1.24))
        timeline.add(time + offset * 1.164, Hit(Note(note).shift_down_octave(1), duration * 1.06))

print("Rendering audio...")
data = timeline.render()
#data = effect.chorus(data, 0.07)
data = effect.shimmer(data, 2.4)
#data = effect.modulated_delay(data, data, 0.004, 0.26)

# Reduce volume to 25%
#data = data * 0.25

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

playback.play(data)