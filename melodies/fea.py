# Je n'est vivre

import os, math
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = random.randint(12, 46)
increment = math.sin(0.19750)
timeline = Timeline()

measure_duration = 36.00
half_measure = measure_duration/2
duration = measure_duration/4
whole_note = duration
three_quarter_note = duration * 0.75
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([0,2,4]))).note
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
  timeline.add(time + 0.0067 + math.sin(increment), Hit(Note(notes[0]), duration))
  timeline.add(time + 0.0073 + math.sin(increment), Hit(Note(notes[3]), duration))
  timeline.add(time + 0.0084 + math.cos(increment), Hit(Note(notes[top]), duration))
      
def strum(time, offset = 0.0035):
  for j, note in enumerate(notes):
      timeline.add(time + offset * math.cos(j) + math.sin(increment), Hit(Note(note), duration))
  
for i in range(iterations):
  strum(time, 0.0037 * math.cos(i))
  time += sixteenth_note
  triad(time)
  time += half_note + math.cos(increment) * math.sin(increment)
  increment += 0.02

print("Rendering audio...")
data = timeline.render(2)
data = effect.tremolo(data, freq=7.7)
data = effect.simple_delay(data)
data = effect.reverb(data)
data = effect.echo(data)
data = effect.shimmer_wobble(data)

data = data * 0.10

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)