import os, math
import time as thetime
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
increment = random.uniform(0.025, 0.64) + math.cos(thetime.time()) * math.sin(0.19750)
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = random.randint(24, 96)
timeline = Timeline()

measure_duration = 26.00
half_measure = measure_duration/2
duration = measure_duration/4
whole_note = duration
three_quarter_note = duration * 0.75
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([0,2,3,4]))).note
key = Note(key_note)

scales = ['japanese', 'major', 'ionian', 'mixolydian', 'phrygian', 'major', 'japanese', 'ionian', 'augmented', 'augmentedfifth', 'melodicminor']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
notes_with_intervals = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(r_scale)

def strum_chord(time, notes):
  timeline.add(time + 0.2, Hit(Note(notes[0]).shift_down_octave(1), three_quarter_note))
  for j, note in enumerate(notes):
      jump = random.uniform(0.02, 1.3)
      timeline.add(time + jump * j + math.sin(increment), Hit(Note(note).shift_down_octave(0), half_note))

def strum_chord_back(time, notes):
  timeline.add(time + 0.2, Hit(Note(notes[0]).shift_down_octave(0), three_quarter_note))
  for j, note in enumerate(notes[::-1]):
      jump = random.uniform(0.04, 1.1)
      if j > 0 and j % 10 == 0:
        timeline.add(time + jump * j + math.cos(increment), Hit(Note(note), half_measure))
      else:
        timeline.add(time + jump * j + math.cos(increment), Hit(Note(note).shift_down_octave(1), half_note))

# pause to start
time += 0.472 + random.uniform(1.3, 2.7)

for i in range(iterations * 8):
  strum_chord_back(time, notes)
  waiter = random.uniform(0.07, 0.86)
  increment += math.cos(waiter)

  if random.randint(2, 22) > 8:
    random.shuffle(notes)
  
  strum_chord(time, notes)
  waiter = random.uniform(0.02, 1.24)
  time += math.sin(waiter)

print("Rendering audio...")
data = timeline.render()
data = effect.modulated_delay(data, data * 0.25, 0.05, 0.02)
data = effect.shimmer_wobble(data)
data = effect.simple_delay(data)

data = data * 0.05

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)