from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, add_intervals_to_notes
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = 5
duration = 4.0
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([1,2,3,4,5]))).note
key = Note(key_note)

scales = ['pentatonicmajor', 'mixolydian', 'phrygian', 'japanese', 'pentatonicminor', 'pentatonicmajor']
random.shuffle(scales)
scale = Scale(key, scales[0])
notes = notes_from_scale(key.note, scale.intervals)
notes_with_intervals = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(scale)
pp.pprint(notes)
pp.pprint(notes_with_intervals)

# Start with all notes on 0
for i, note in enumerate(notes_with_intervals):
    timeline.add(time, Hit(Note(note[0]), duration))
    #time += duration / 2

for i in range(2):
    for j, note in enumerate(notes_with_intervals):
        timeline.add(time + note[1], Hit(Note(note[0]), duration))
    time += duration


print("Rendering audio...")
data = timeline.render()
data = effect.chorus(data, 0.75)

print("Playing audio...")
playback.play(data)