from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = 5
duration = 4.0
timeline = Timeline()

# Define key and scale
key = Note('C')
scale = Scale(key, 'chromatic')
notes = notes_from_scale(key.note, scale.intervals)

pp.pprint(notes)

# Start with all notes on 0
for i, note in enumerate(notes):
    timeline.add(time, Hit(Note(note), duration))
    time += duration / 2

# each note has its own speed
for i, note in enumerate(notes):
    time += 0.5
    timeline.add(time, Hit(Note(note), duration))

print("Rendering audio...")
data = timeline.render()
data = effect.chorus(data, 0.75)

print("Playing audio...")
playback.play(data)