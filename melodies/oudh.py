# Je n'est vivre

# To keep: oudh, pppony, Bb-asc/desc, slow
# To run: venv/bin/python3.12 melodies/stepping.py


from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = 5
duration = 4.0
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([0, 1, 2, 3, 4]))).note
key = Note(key_note)

#scales = ['chromatic']
scales = ['major', 'pentatonicmajor', 'japanese', 'diminished', 'locrian', 'ionian', 'mixolydian', 'phrygian']


# todo: use Ara melodies?
# todo: more notes in notes_from_scale
# todo: add interval to notes should pass a param that starts at 0.0 and increases (0.1, 0.2) etc, incl option to add noise to the increments)

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = notes_from_scale(key.note, scale.intervals)
notes_with_intervals = add_intervals_to_notes(notes)
pp.pprint(key)
pp.pprint(r_scale)

# Ascending arpeggio to open
for j, note in enumerate(notes):
    timeline.add(time + 0.1, Hit(Note(note), duration))
time += duration
    
for i in range(75):
    for j, note in enumerate(notes_with_intervals):
        interval = add_random_float(note[1], -1.25, 2.75)
        timeline.add(time + interval, Hit(Note(note[0]), duration))
    time += duration
    
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = notes_from_scale(key.note, scale.intervals)
notes_with_intervals = add_intervals_to_notes(notes)
pp.pprint(key)
pp.pprint(r_scale)

# And breathe....
time += duration * 2

for i in range(25):
    for j, note in enumerate(notes_with_intervals):
        interval = add_random_float(note[1], -0.25, 4.75)
        timeline.add(time + interval, Hit(Note(note[0]), duration))
    time += duration
    
# Descending arppegio to close
for j, note in enumerate(notes[::-1]):
    timeline.add(time + 0.1, Hit(Note(note), duration))
time += duration


print("Rendering audio...")
data = timeline.render()
data = effect.tremolo(data, freq=1.47)
data = effect.modulated_delay(data, data, 0.02, 0.03)
data = effect.reverb(data, 0.8, 0.425)
data = effect.flanger(data, 0.04)

print("Playing audio...")
playback.play(data)