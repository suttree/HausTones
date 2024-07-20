import os, math
import time as thetime
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = random.randint(4, 32)
duration = 4.0
timeline = Timeline()

measure_duration = 24.00
half_measure = measure_duration/2
duration = measure_duration/4
whole_note = duration
three_quarter_note = duration * 0.75
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([1,2,3]))).note
key = Note(key_note)

scales = ['augmentedfifth', 'aeolian', 'harmonicminor', 'diminished', 'dorian']
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
notesi = add_intervals_to_notes(notes)
pp.pprint(key)
pp.pprint(r_scale)

time += sixteenth_note + random.uniform(0.8, 4.4)

for i in range(iterations):

  for j, note in enumerate(notes[::3]):
    inc = time + eighth_note + math.sin(thetime.time())
    timeline.add(inc, Hit(Note(note[0]), duration/2))
    time += 0.15

    for k, note in enumerate(notes[::-5]):
      timeline.add(time + eighth_note, Hit(Note(note), duration*2))
      time += 0.3

      for l, note in enumerate(notes[::4]):
        inc = time + eighth_note + math.cos(thetime.time())
        timeline.add(inc, Hit(Note(note), duration*2))
        time += 0.25

    if j % 2 == 0:
      time += duration/2

  if i % 5 == 0:
    time -= 0.75

  random.shuffle(notes)

time += sixteenth_note + random.uniform(0.8, 4.4)

print("Rendering audio...")
data = timeline.render()

#data = data * 0.85

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)