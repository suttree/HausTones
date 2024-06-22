import os, math
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0 
offset = 0.0
iterations = random.randint(6, 26)
duration = 4.0
timeline = Timeline()

measure_duration = 32.00
half_measure = measure_duration/2
duration = measure_duration/4
whole_note = duration
three_quarter_note = duration * 0.75
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([2]))).note
key = Note(key_note)

scales = ['major', 'japanese', 'ionian', 'augmented', 'augmentedfifth', 'melodicminor']
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 0)
pp.pprint(key)
pp.pprint(r_scale)

def reset():
  key_note = Note((random.choice(Note.NOTES), random.choice([0]))).note
  key = Note(key_note)
  r_scale = random.choice(scales)
  scale = Scale(key, r_scale)
  notes = notes_from_scale(key.note, scale.intervals)
  pp.pprint(key)
  pp.pprint(r_scale)

for i in range(iterations):
  random.shuffle(notes)
  for i in range(3):
    timeline.add(time, Hit(Note(notes[i]), measure_duration))
    time += duration
  time += sixteenth_note
  reset()
  
print("Rendering audio...")
data = timeline.render()
data = effect.echo(data)
data = effect.simple_delay(data, 250, 0.28, 0.977)

# Reduce volume to 25%
data = data * 0.25

#from musical.utils import save_normalized_audio
#save_normalized_audio(data, 44100, os.path.basename(__file__))

playback.play(data)