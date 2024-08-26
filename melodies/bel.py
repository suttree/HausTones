# Je n'est vivre

# To keep: oudh, pppony, Bb-asc/desc, slow
# To run: venv/bin/python3.12 melodies/stepping.py

# todo: use Ara melodies?
# todo: more notes in notes_from_scale
# todo: add interval to notes should pass a param that starts at 0.0 and increases (0.1, 0.2) etc, incl option to add noise to the increments)

# TODO: test the asc and desc parts individually, get them working
# TODO: export to wav for playback later

import os, math, time
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = random.randint(12, 33)
duration = 4.0
timeline = Timeline()
increment = random.uniform(0.2, 0.82) + math.sin(0.19750)

measure_duration = 64.00
half_measure = measure_duration/2
duration = measure_duration/4
whole_note = duration
three_quarter_note = duration * 0.75
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([2,3]))).note
key = Note(key_note)
#key = Note('a4')
scales = ['ionian']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
notesi = add_intervals_to_notes(notes)
pp.pprint(key)
pp.pprint(r_scale)

def triad(time):
  timeline.add(time + 0.062 + math.sin(increment), Hit(Note(notes[0]), duration))
  timeline.add(time + 0.073 + math.sin(increment), Hit(Note(notes[2]), duration))
  timeline.add(time + 0.084 + math.cos(increment), Hit(Note(notes[2]), duration))
      
def strum(time, offset = 0.035):
  #timeline.add(time + sixteenth_note, Hit(Note(notes[0]).shift_down_octave(1), duration))
  for j, note in enumerate(notes):
      timeline.add(time + offset * math.cos(j) + math.sin(increment), Hit(Note(note), duration))

def reset():
  key_note = Note((random.choice(Note.NOTES), random.choice([2,3]))).note
  key = Note(key_note)
  r_scale = random.choice(scales)
  scale = Scale(key, r_scale)
  notes = notes_from_scale(key.note, scale.intervals)
  return notes
  
time += sixteenth_note + random.uniform(0.5, 2.2)

# Descending arppegio
for i in range(7):
  for j, note in enumerate(notes[::-3]):
    #timeline.add(time + 0.2 * j*i, Hit(Note(note), duration))
    if i > 0 and j % 3 == 0 and j > 0:
      strum(time, 1.287 * math.cos(i))
      time += sixteenth_note
  time += half_note + (1 * math.cos(increment))
    
  for x in range(7)[::4]:
    timeline.add(time + 0.22 * j*i*x, Hit(Note(note), duration/2))

  if i % 3 == 0 and i > 0:
    random.shuffle(notes)

  #triad(time)
  #time += half_note + (1 * math.cos(increment)) * math.sin(increment)

  #if i < 4:
  #  timeline.add(time + math.sin(time), Hit(Note(notes[0]).shift_down_octave(1), duration/2))

  increment += 0.0028 + math.sin(time)
  time += 0.025

print("Rendering audio...")
data = timeline.render()
#data = effect.feedback_modulated_delay(data, data, 0.6, 0.06)
#data = effect.tremolo(data, freq=7.7)
data = effect.simple_delay(data)
#data = effect.reverb(data)
data = effect.echo(data)
#data = effect.shimmer_wobble(data)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)