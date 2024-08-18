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
iterations = random.randint(18, 72)
duration = 4.0
increment = random.uniform(0.025, 0.64) + math.cos(thetime.time()) * math.sin(0.19750)
timeline = Timeline()

measure_duration = 14.00
half_measure = measure_duration/2
duration = measure_duration/4
whole_note = duration
three_quarter_note = duration * 0.75
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([1]))).note
key = Note('a#4')

scales = ['ionian', 'phrygian', 'ionian', 'augmentedfifth', 'melodicminor']
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 1)
notes_with_intervals = add_intervals_to_notes(notes)
pp.pprint(key)
pp.pprint(r_scale)

def play_triad(time):
  timeline.add(time + 0.0042 + math.sin(increment), Hit(Note(notes[0]), duration))
  timeline.add(time + 0.0062 + math.cos(increment), Hit(Note(notes[3]), duration))
  timeline.add(time + 0.0074 + math.sin(increment), Hit(Note(notes[3]), duration))
      
def strum_chord(time):
  for j, note in enumerate(notes):
      timeline.add(time + 0.0055 * j + math.sin(increment), Hit(Note(note), duration))

time += sixteenth_note + random.uniform(0.8, 2.4)

for i in range(iterations):
  # nice chord
  for j, note in enumerate(notes[::-1]):
      timeline.add(time+0.0075*j+1, Hit(Note(note), measure_duration))
      
  for j, note in enumerate(notes[::-4]):
    timeline.add(time + 0.25*j*2, Hit(Note(note), measure_duration))
    for j, note in enumerate(notes[::3]):
      timeline.add(time + 0.25*j*2, Hit(Note(note), measure_duration))
      time -= 0.24
  time += half_measure + math.cos(thetime.time())

  if (i % 2 == 0 and i > 0):
    random.shuffle(notes)

  play_triad(time)
  time += duration/16 + 1 * math.sin(i)
  strum_chord(time)
  time += duration/16 + 0.52 * math.cos(increment)

time += sixteenth_note * math.cos(thetime.time())

print("Rendering audio...")
data = timeline.render()

data = effect.feedback_modulated_delay(data, data * 0.25, 0.5, 0.2)
data = effect.simple_delay(data, 1500)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)
