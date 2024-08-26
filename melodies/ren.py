import os, math, time
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
increment = math.sin(0.27843) * math.cos(time.time())
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.1
iterations = random.randint(12, 46)
duration = 44.5
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([0,1,2]))).note
random_note = random.choice(['g#4', 'd#4'])
key = Note(random_note)

scales = ['major', 'ionian', 'mixolydian', 'phrygian', 'major', 'japanese', 'ionian', 'augmented', 'augmentedfifth', 'melodicminor']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = notes_from_scale(key.note, scale.intervals)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
notes_with_intervals = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(r_scale)

measure_duration = 48.00
half_measure = measure_duration/2
duration = measure_duration/4
whole_note = duration
three_quarter_note = duration * 0.75
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

def reset():
  key_note = Note((random.choice(Note.NOTES), random.choice([2,3]))).note
  key = Note(key_note)
  r_scale = random.choice(scales)
  scale = Scale(key, r_scale)
  notes = notes_from_scale(key.note, scale.intervals)
  random.shuffle(notes)
  return notes

def play_triad(time, reveresed = 0):
  if reversed:
    timeline.add(time + 0.0062 + math.sin(increment), Hit(Note(notes[5]).shift_down_octave(1), duration))
    timeline.add(time + 0.0062 + math.sin(increment), Hit(Note(notes[5]), duration))
    timeline.add(time + 0.0062 + math.sin(increment), Hit(Note(notes[3]), duration))
    timeline.add(time + 0.0062 + math.sin(increment), Hit(Note(notes[0]), duration))
  else:
    timeline.add(time + 0.0062 + math.sin(increment), Hit(Note(notes[0]).shift_down_octave(1), duration))
    timeline.add(time + 0.0062 + math.sin(increment), Hit(Note(notes[0]), duration))
    timeline.add(time + 0.0062 + math.sin(increment), Hit(Note(notes[3]), duration))
    timeline.add(time + 0.0062 + math.sin(increment), Hit(Note(notes[5]), duration))
      
def strum_chord(time, notes):
  if random.choice([1,2,3,4,5,6]) > 5:
    notes = notes[::-1]
  else:
    notes = notes

  random_note = random.choice(notes)
  notes.remove(random_note)
  
  for j, note in enumerate(notes):
      timeline.add(time + 0.092 * j + math.sin(increment), Hit(Note(note), duration))
      
  notes.append(random_note)

time += 0.44 + random.uniform(0.6, 2.4)

for i in range(iterations):
  for i in range(3):
    strum_chord(time, notes)
    time += eighth_note * math.sin(i)
    
  time += duration/16 + 1 * math.sin(i)
  
  for i in range(2):
    if i % 2 == 0:
      reversed = 1
    else:
      reversed = 0
    play_triad(time, reversed)
    time += 0.22 + math.sin(increment)

  if i % 4 == 0:
    notes = reset()

  time += duration/8 + math.cos(increment) * math.sin(increment)

print("Rendering audio...")
data = timeline.render()
data = effect.shimmer_wobble(data, 0.2)

#data = data * 0.25

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)
