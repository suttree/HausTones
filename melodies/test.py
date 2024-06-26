# Je n'est vivre

# To keep: oudh, pppony, Bb-asc/desc, slow
# To run: venv/bin/python3.12 melodies/stepping.py

# todo: use Ara melodies?
# todo: more notes in notes_from_scale
# todo: add interval to notes should pass a param that starts at 0.0 and increases (0.1, 0.2) etc, incl option to add noise to the increments)

# TODO: test the asc and desc parts individually, get them working
# TODO: export to wav for playback later


from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = 2
duration = 4.0
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([0, 1, 2, 3]))).note
key = Note(key_note)

scales = ['chromatic','major', 'pentatonicmajor']
#scales = ['major', 'pentatonicmajor', 'japanese', 'diminished', 'locrian', 'ionian', 'mixolydian', 'phrygian']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
notes_with_intervals = add_intervals_to_notes(notes)
pp.pprint(key)
pp.pprint(r_scale)


# CROSS OVER
## Ascending
#for j, note in enumerate(notes):
#  timeline.add(time + 0.25*j*2, Hit(Note(note), duration*2))
## Descending arppegio
#for j, note in enumerate(notes[::-1]):
#  timeline.add(time + 0.25*j*2, Hit(Note(note), duration))
#time += duration

# Define key and scale
time = 0.0 # Keep track of currect note placement time in seconds
offset = 0.4286
iterations = 4
duration = 4.286 # 140bpm

key = Note('C')
scale = Scale(key, 'pentatonicmajor')
notes = notes_from_scale(key.note, scale.intervals)

# fuzzy repeater
for i in range(iterations):
    for j, note in enumerate(notes[::-1]):
        timeline.add(time+0.075*j, Hit(Note(note), duration))
    time += duration

    for n in range(8):
      for j, note in enumerate(notes[::-1]):
          timeline.add(time + offset * j, Hit(Note(note), duration))
          timeline.add(duration/4 + time + offset * j, Hit(Note(note), duration))
      time += duration/2

    # Cavernous ascender
    for j, note in enumerate(notes):
        timeline.add(time+0.95*j, Hit(Note(note), duration*2))
    time += duration


print("Rendering audio...")
data = timeline.render()
data = effect.shimmer(data, 0.24)
data = effect.tremolo(data, 0.1)
data = effect.reverb(data, 0.8, 0.025)

#data = data * 0.25
#data = timeline.render() #hah

print("Playing audio...")
playback.play(data)