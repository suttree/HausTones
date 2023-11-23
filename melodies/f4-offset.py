from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline

from musical.utils import notes_from_scale

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
offset = 0.0
iterations = random.randint(8, 64)
duration = 4.286
timeline = Timeline()

# Define key and scale
key = Note('F4')
scale = Scale(key, 'chromatic')
notes = notes_from_scale(key.note, scale.intervals)

for i in range(iterations):
    for j, note in enumerate(notes[::-1]):
        timeline.add(time + offset * j, Hit(Note(note), duration))
    time += 1.286

    if(offset > 1.2):
        offset -= 0.02
    elif(offset < 0.1):
        offset += 0.02
    else:
        offset += 0.02

    if(i % 12 == 0):
        timeline.add(time + offset, Hit(Note(note).shift_down_octave(1), duration * 2))
        timeline.add(time + offset, Hit(Note(note).shift_down_octave(1), duration * 3))
        timeline.add(time + offset, Hit(Note(note).shift_down_octave(2), duration * 4))
        timeline.add(time + offset, Hit(Note(note).shift_down_octave(2), duration * 5))

print("Rendering audio...")
data = timeline.render()
#data = effect.chorus(data, 0.07)
#data = effect.modulated_delay(data, data, 0.004, 0.26)

# Reduce volume to 25%
data = data * 0.25

print("Playing audio...")
playback.play(data)