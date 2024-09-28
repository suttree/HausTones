# Je n'est vivre

import os, math, time
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
increment = random.uniform(0.2, 0.82) + math.cos(time.time()) * math.sin(0.19750)
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.25
iterations = random.randint(12, 46)
timeline = Timeline()

measure_duration = 84.00
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

scales = ['major', 'mixolydian', 'phrygian', 'augmented', 'augmentedfifth', 'melodicminor']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
notes_with_intervals = add_intervals_to_notes(notes)

def reset():
  key_note = Note((random.choice(Note.NOTES), random.choice([2,3]))).note
  key = Note(key_note)
  r_scale = random.choice(scales)
  scale = Scale(key, r_scale)
  notes = notes_from_scale(key.note, scale.intervals)
  return notes

pp.pprint(key)
pp.pprint(r_scale)

time += sixteenth_note + random.uniform(0.2, 0.8)

intervals = [-4, -3, -2, 2, 3, 4]

notes = extended_notes_from_scale(key.note, scale.intervals, 2)  

for i in range(iterations):  
  if i % 3 == 0 and i > 0:
    random.shuffle(intervals)

  timeline.add(time + eighth_note, Hit(Note(notes[0]), duration))
  for j, note in enumerate(notes[::intervals[0]]):
    timeline.add(time + eighth_note, Hit(Note(note), duration))
    time += 1.0 
    
    if time % 4 == 0 and time > 0:
      time += math.sin(time)

    timeline.add(time + eighth_note, Hit(Note(notes[-1]), duration))
    
    for j, note in enumerate(notes[::intervals[-1]]):
      timeline.add(time + eighth_note, Hit(Note(note), duration + math.cos(j)))
      
      if i % 3 == 0 and i > 0:
        time += 0.072 + math.sin(j)

  time += 1.0

  if i % 6 == 0 and i > 0:
    notes = reset()
    
  if i % 18 == 0 and i > 0:
    time -= math.cos(time)

print("Rendering audio...")
data = timeline.render(13)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)
