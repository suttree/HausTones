from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline

from musical.utils import notes_from_scale

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
offset = 0.4286
iterations = random.randint(6, 32)
duration = 4.286 # 140bpm
timeline = Timeline()

# Define key and scale
key = Note('C')
scale = Scale(key, 'pentatonicmajor')
notes = notes_from_scale(key.note, scale.intervals)

for i in range(iterations):
    for j, note in enumerate(notes[::-1]):
        timeline.add(time + offset * j, Hit(Note(note), duration))
    time += duration/2
        
print("Rendering audio...")
data = timeline.render()
data = effect.tremolo(data, 0.1)
data = effect.reverb(data, 0.8, 0.025)

# Reduce volume to 25%
#data = data * 0.25

print("Playing audio...")
playback.play(data)