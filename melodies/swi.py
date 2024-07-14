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
offset = 0.49
iterations = random.randint(12, 46)
#iterations = random.randint(1, 4)
timeline = Timeline()

measure_duration = 30.00
half_measure = measure_duration/2,
duration = measure_duration/4
whole_note = duration
three_quarter_note = duration * 0.75
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([0,2,4,5]))).note
key = Note(key_note)

scales = ['japanese', 'major', 'ionian', 'mixolydian', 'phrygian', 'major', 'japanese', 'ionian', 'augmented', 'augmentedfifth', 'melodicminor']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 3)
notes_with_intervals = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(r_scale)

def triad(time):
  top = random.choice([0,2,3,5])
  timeline.add(time + 0.587 + math.sin(increment), Hit(Note(notes[3]), duration))
  timeline.add(time + 0.833 + math.cos(increment), Hit(Note(notes[top]), duration))
  timeline.add(time + 0.907 + math.sin(increment), Hit(Note(notes[0]), duration))


def double(time):
  top = random.choice([1,3,4])
  timeline.add(time + 0.564 + math.cos(offset), Hit(Note(notes[top]), duration))
  timeline.add(time + 0.728 + math.cos(increment), Hit(Note(notes[0]), duration))
  
def strum(time, offset = 0.0035):
  for j, note in enumerate(notes[::-3]):
      timeline.add(time + offset * math.cos(j) + math.sin(increment), Hit(Note(note), duration))

time += 0.37 + random.uniform(0.6, 3.2)

for i in range(iterations):
  strum(time, 0.0047 * math.cos(i))
  time += three_quarter_note + math.sin(increment) * math.cos(thetime.time())

  if i > 0:
    if i % 4 == 0:
      double(time)
      time += three_quarter_note + math.sin(increment) * math.cos(increment)

    if i % 12 == 0:
      random.shuffle(notes)

  triad(time)
  time += half_note + math.cos(increment) * math.sin(increment)
  increment += 0.2
  


time += 0.37 + random.uniform(1.2, 2.3) + math.cos(thetime.time())

print("Rendering audio...")
data = timeline.render()
data = effect.simple_delay(data * 0.74)
data = effect.reverb(data * 0.33)
data = effect.chorus(data * 0.5, freq=0.49)
#data = effect.echo(data)
#data = effect.shimmer_wobble(data)

#data = data * 0.15

#from musical.utils import save_normalized_audio
#save_normalized_audio(data, 44100, os.path.basename(__file__))

playback.play(data)