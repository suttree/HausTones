# Je n'est vivre

import os, math, time
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
increment = math.sin(0.19750) * math.cos(time.time())
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = random.randint(12, 46)
duration = 42.0
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([0]))).note
key = Note(key_note)

scales = ['japanese', 'major', 'ionian', 'mixolydian', 'phrygian', 'major', 'japanese', 'ionian', 'augmented', 'augmentedfifth', 'melodicminor']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
#notes = notes_from_scale(key.note, scale.intervals)
notes = notes_from_scale(key.note, scale.intervals)
notes = extended_notes_from_scale(key.note, scale.intervals, 1)
notes_with_intervals = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(r_scale)

def play_triad(time):
  timeline.add(time + 0.0062 + math.sin(increment), Hit(Note(notes[0]), duration))
  timeline.add(time + 0.0062 + math.sin(increment), Hit(Note(notes[3]), duration))
  timeline.add(time + 0.0064 + math.sin(increment), Hit(Note(notes[5]), duration))
      
def strum_chord(time):
  for j, note in enumerate(notes):
      timeline.add(time + 0.0035 * j + math.sin(increment), Hit(Note(note), duration))

time += 0.24 + random.uniform(4.2, 6.4)

for i in range(iterations):
  strum_chord(time)
  time += duration/16 + 1 * math.sin(i)
  play_triad(time)
  time += duration/16 + math.cos(increment) * math.sin(increment)

print("Rendering audio...")
data = timeline.render()
data = effect.reverb(data, 0.28, 0.525)
data = effect.echo(data)

data = data * 0.25

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)
