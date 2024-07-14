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
increment = random.uniform(0.2, 0.82) + math.cos(thetime.time()) * math.sin(0.19750)
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.25
iterations = random.randint(12, 36)
timeline = Timeline()

measure_duration = 52.00
half_measure = measure_duration/2
duration = measure_duration/4
whole_note = duration
three_quarter_note = duration * 0.75
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([0,1,2,3]))).note
key = Note(key_note)

scales = ['japanese', 'major', 'ionian', 'mixolydian', 'phrygian', 'major', 'japanese', 'ionian', 'augmented', 'augmentedfifth', 'melodicminor']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
notes_with_intervals = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(r_scale)

def triad(time):
  timeline.add(time + 0.062 + math.sin(increment), Hit(Note(notes[1]), duration))
  timeline.add(time + 0.073 + math.sin(increment), Hit(Note(notes[3]), duration))
  timeline.add(time + 0.084 + math.cos(increment), Hit(Note(notes[4]), duration))
      
def strum(time, offset = 0.035):
  for j, note in enumerate(notes):
      timeline.add(time + offset * math.cos(j) + math.sin(increment), Hit(Note(note), duration))
  timeline.add(time +  2.0, Hit(Note(notes[0]), duration/2))

def strum2(time, offset = 0.3417):
  for j, note in enumerate(notes[::-4]):
      timeline.add(time + offset * 0.25 + math.cos(j), Hit(Note(note), duration))
  timeline.add(time +  1.0, Hit(Note(notes[0]).shift_down_octave(1), duration/2))
      
time += sixteenth_note + random.uniform(1.5, 6.2)

for i in range(iterations):
  strum(time, 0.037 * math.cos(i))
  time += quarter_note
  strum2(time, 0.3417 * math.sin(thetime.time()))
  time += half_note + (1 * math.cos(increment)) * math.sin(increment)
  increment += 0.028 * math.cos(thetime.time())
  
  if i % iterations/2 == 0:
    random.shuffle(notes)

time += 0.37 + random.uniform(0.9, 4.4)

print("Rendering audio...")
data = timeline.render()
data = effect.reverb(data * 0.60)
#data = effect.echo(data)
data = effect.tremolo(data * 0.80, freq=0.314)
data = effect.simple_delay(data * 0.25, 25)
#data = effect.shimmer_wobble(data)
#data = data * 0.25

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)