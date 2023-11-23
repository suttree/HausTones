from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from musical.utils import notes_from_scale

from timeline import Hit, Timeline

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
timeline = Timeline()
interval = random.uniform(0.2, 0.6)
offset = interval + random.uniform(0.1, 0.3)
offset_i = 0.0
iterations = random.randint(6, 48)
duration = random.uniform(1.0, 8.0)

# Define key and scale
key = Note(random.choice(Note.NOTES))
scale = Scale(key, 'chromatic')
notes = notes_from_scale(key.note, scale.intervals)

for i in range(iterations):
    for j, note in enumerate(notes[::-1]):
        note = Note(note)

        timeline.add(time + offset_i * j, Hit(note, duration))
    time += random.uniform(1.0, 2.0) #1.25
    offset_i += random.uniform(0.1, 0.2) #0.125
        
print("Rendering audio...")
data = timeline.render()
data = effect.tremolo(data, 0.1)

# Reduce volume to 25%
data = data * 0.25

print("Playing audio...")
playback.play(data)