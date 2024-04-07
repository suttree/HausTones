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
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = notes_from_scale(key.note, scale.intervals)
notes_with_intervals = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(r_scale)
pp.pprint(notes)

# todo: use Ara melodies?
# todo: more notes in notes_from_scale
# todo: add interval to notes should pass a param that starts at 0.0 and increases (0.1, 0.2) etc, incl option to add noise to the increments)
# can i switch scale after x number of iterations? with a arpeggio to indicate the end/beginning

for i in range(25):
    for j, note in enumerate(notes_with_intervals):
        interval = add_random_float(note[1], -1.25, 2.75)
        timeline.add(time + interval, Hit(Note(note[0]), duration))
        pp.pprint([note[0], interval])
    time += duration

print("Rendering audio...")
data = timeline.render()
data = effect.tremolo(data, freq=1.1)
#data = effect.modulated_delay(data, data, 0.2, 1.8)
data = effect.reverb(data, 0.8, 0.025)

print("Playing audio...")
playback.play(data)