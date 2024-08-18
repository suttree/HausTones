import os, math
import time as thetime
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0
offset = 0.0
#iterations = random.randint(18, 72)
iterations = 3
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
notesi = add_intervals_to_notes(notes)
progression = Chord.progression(scale)
chord = progression[0]
pp.pprint(key)
pp.pprint(r_scale)

def reset():
  key_note = Note((random.choice(Note.NOTES), random.choice([2,3]))).note
  key = Note(key_note)
  r_scale = random.choice(scales)
  scale = Scale(key, r_scale)
  notes = notes_from_scale(key.note, scale.intervals)
  random.shuffle(notes)

def strum(time, offset = 0.035):
  for j, note in enumerate(notes):
      timeline.add(time + offset * math.cos(j) + math.sin(increment), Hit(Note(note), measure_duration))

def double(time):
  top = random.choice([1,2,4])
  timeline.add(time + 0.2 + math.cos(offset), Hit(Note(notes[top]), duration))
  timeline.add(time + 0.4 + math.cos(increment), Hit(Note(notes[0]), duration))
  
time += sixteenth_note + random.uniform(1.5, 2.2)

for i in range(iterations):
  time += sixteenth_note
  random.shuffle(notes)
  strum(time, 0.037 * math.cos(i))
  time += sixteenth_note
  
  double(time)
  time += three_quarter_note + math.sin(increment) * math.cos(increment)

  reset()
  offset += math.sin(time)

time += sixteenth_note * math.cos(thetime.time())

print("Rendering audio...")
data = timeline.render()

#data = effect.modulated_delay(data, data * 0.25, 0.5, 0.2)
#data = effect.simple_delay(data, 1500)
data = effect.shimmer_wobble(data)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)
