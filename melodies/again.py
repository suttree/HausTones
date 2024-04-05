from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale
import pprint, random
import numpy as np

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = 5
duration = 4.0

# Define key and scale
key = Note('C')
scale = Scale(key, 'chromatic')
notes = notes_from_scale(key.note, scale.intervals)

pp.pprint(notes)

# Create a list to store the timelines for each note
timelines = []

# Create a separate timeline for each note
for i, note in enumerate(notes):
    timeline = Timeline()
    interval = 1.0 + i * 0.1  # Calculate the interval for each note
    time = 0.0
    
    while time < duration:
        timeline.add(time, Hit(Note(note), 0.5))  # Adjust the duration as needed
        time += interval
    
    timelines.append(timeline)

# Render audio from each timeline
print("Rendering audio...")
renders = [timeline.render() for timeline in timelines]

# Find the maximum length among the renders
max_length = max(len(render) for render in renders)

# Pad the renders with zeros to match the maximum length
padded_renders = [np.pad(render, (0, max_length - len(render))) for render in renders]

# Normalize the audio data
normalized_renders = [render / np.max(np.abs(render)) for render in padded_renders]

# Sum the normalized renders
data = sum(normalized_renders)

# Apply the chorus effect
data = effect.chorus(data, 0.75)

print("Playing audio...")
playback.play(data)