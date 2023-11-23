from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline

from musical.utils import notes_from_scale

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
offset = 0.4286
iterations = random.randint(6, 22)
duration = 4.286 # 140bpm
timeline = Timeline()

# Define key and scale
key = Note('Bb')
scale = Scale(key, 'chromatic')
notes = notes_from_scale(key.note, scale.intervals)

for i in range(iterations):
    for j, note in enumerate(notes):
        timeline.add(time + offset * j, Hit(Note(note), duration))
    time += duration
        
print("Rendering audio...")
data = timeline.render()
data = effect.chorus(data, 0.1)

# Reduce volume to 25%
data = data * 0.25

print("Playing audio...")
playback.play(data)