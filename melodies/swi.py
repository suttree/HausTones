# Je n'est vivre

import os, math
import time as thetime
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
increment = random.uniform(0.02, 0.84) + math.cos(thetime.time()) * math.sin(0.19750)
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = random.randint(12, 46)
timeline = Timeline()

measure_duration = 32.00
half_measure = measure_duration/21,
duration = measure_duration/4
whole_note = duration
three_quarter_note = duration * 0.75
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([0,1,2,3,4,5]))).note
key = Note(key_note)

scales = ['japanese', 'major', 'ionian', 'mixolydian', 'phrygian', 'major', 'japanese', 'ionian', 'augmented', 'augmentedfifth', 'melodicminor']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
notes_with_intervals = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(r_scale)

def triad(time):
  top = random.choice([0,2,3,5])
  timeline.add(time + 0.087 + math.sin(increment), Hit(Note(notes[0]), duration))
  timeline.add(time + 0.093 + math.sin(increment), Hit(Note(notes[3]), duration))
  timeline.add(time + 0.124 + math.cos(increment), Hit(Note(notes[top]), duration))

def double(time):
  top = random.choice([1,3,4])
  timeline.add(time + 0.044 + math.cos(increment), Hit(Note(notes[0]), duration))
  timeline.add(time + 0.048 + math.cos(offset), Hit(Note(notes[top]), duration))
  
def strum(time, offset = 0.0035):
  for j, note in enumerate(notes[::-1]):
      timeline.add(time + offset * math.cos(j) + math.sin(increment), Hit(Note(note), duration))

time += 0.37 + random.uniform(0.8, 3.4)

for i in range(iterations):
  strum(time, 0.0047 * math.cos(i))
  time += three_quarter_note + math.sin(increment) * math.cos(random.randint(1,3))

  if random.randint(0,6) > 4:
    double(time)
    time += three_quarter_note + math.sin(increment) * math.cos(increment)

  triad(time)
  time += half_note + math.cos(increment) * math.sin(increment)
  increment += 0.2

print("Rendering audio...")
data = timeline.render()
data = effect.simple_delay(data)
data = effect.reverb(data)
data = effect.echo(data)
data = effect.shimmer_wobble(data)

data = data * 0.15

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)