from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from musical.utils import notes_from_scale

from timeline import Hit, Timeline

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
timeline = Timeline()
interval = random.uniform(1.2, 2.6)
offset_i = random.uniform(0.08, 0.137)
iterations = random.randint(12, 64)
duration = random.uniform(6.0, 18.0)

# Define key and scale
key = Note(random.choice(Note.NOTES))
scale = Scale(key, 'chromatic')
notes = notes_from_scale(key.note + '4', scale.intervals)

if(random.randint(0,1) > 0):
    note_progression = notes[::-1]
else:
    note_progression = notes

for i in range(iterations):
    for j, note in enumerate(note_progression):
        note = Note(note)
        timeline.add(time + offset_i * j, Hit(note, duration))

    time += interval + random.uniform(2.0, 8.0) + offset_i # 2.5 # random.uniform(1.0, 2.0) #1.25

#print "Rendering audio..."
data = timeline.render()

data = effect.chorus(data, 0.17)

# Reduce volume to 10%
data = data * 0.10

#print "Playing audio..."
playback.play(data)