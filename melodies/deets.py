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
iterations = random.randint(4, 8)
duration = 1.3287
measure_duration = 4.626
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([2]))).note
key = Note(key_note)
scale = Scale(key, 'pentatonicmajor')

def reset():
  key_note = Note((random.choice(Note.NOTES), random.choice([2]))).note
  key = Note(key_note)
  scales = ['major', 'pentatonicmajor', 'japanese', 'locrian', 'ionian', 'mixolydian', 'phrygian']
  r_scale = random.choice(scales)
  scale = Scale(key, r_scale)
  notes = extended_notes_from_scale(key.note, scale.intervals, 1)
  #notes = notes_from_scale(key.note, scale.intervals)
  return notes

notes = extended_notes_from_scale(key.note, scale.intervals, 1)
notes_with_intervals = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(scale)

time += 0.38 + random.uniform(0.8, 4.3)

for i in range(10):
  for note in enumerate(notes_with_intervals):
      n = note[1]
      timeline.add(time, Hit(Note(n[0]), measure_duration + math.cos(time)))

      for note in enumerate(notes_with_intervals[::3]):
        n = note[1]
        timeline.add(time, Hit(Note(n[0]).shift_up_octave(1), measure_duration))
      time += duration + math.sin(n[1])

  time += measure_duration - math.cos(time)
  
  if i % 2 == 0 and i > 0:
    random.shuffle(notes_with_intervals)
    
  if i % 4 == 0 and i > 0:
    notes_with_intervals = add_intervals_to_notes(notes[::2])
    
  if i % 6 == 0 and i > 0:
    notes = reset()
    notes_with_intervals = add_intervals_to_notes(notes)
    
  if i % 8 == 0 and i > 0:
    notes_with_intervals = add_intervals_to_notes(notes[::-1])

print("Rendering audio...")
data = timeline.render()
data = effect.tremolo(data, freq=0.79)
data = effect.shimmer_wobble(data, 0.54)

data = data * 0.25

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)
