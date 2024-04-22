# Je n'est vivre

import os, math
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
offset = 0.4286
iterations = 1
duration = 4.286 # 140bpm
increment = duration / 4
timeline = Timeline()
interval = 2

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([1, 2, 3]))).note
key = Note(key_note)

scales = ['major', 'pentatonicmajor', 'diminished', 'phrygian']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 3)
notes_with_intervals = add_intervals_to_notes(notes)
pp.pprint(key)
pp.pprint(r_scale)

for a in range(4):
  #increment -= math.sin(increment)
  #duration -= math.cos(increment)
  for n in range(4):
    #increment -= math.cos(increment)
    #duration -= math.sin(increment)
    for i in range(4):
      #increment -= math.sin(increment)
      #duration -= math.cos(increment)
      for j, note in enumerate(notes_with_intervals[::-8]):
        timeline.add(time + increment, Hit(Note(notes_with_intervals[0][0]), duration))
    
      for j, note in enumerate(notes_with_intervals[::-1]):
        timeline.add(time + math.sin(0.25) * j*i+1, Hit(Note(note[0]), duration))

      time += 2.0 + math.cos(time)
      #duration -= math.cos(increment)
    
      for j, note in enumerate(notes_with_intervals):
          timeline.add(time + math.cos(j)*i*n, Hit(Note(note[0]), duration))

      for j, note in enumerate(notes_with_intervals[::12]):
        timeline.add(time + increment, Hit(Note(notes_with_intervals[-1][0]), duration*2))
      time += duration
      
print("Rendering audio...")
data = timeline.render()
#data = effect.shimmer(data, 0.24)
#data = effect.tremolo(data, 0.042)
#data = effect.reverb(data, 0.8, 0.025)

data = data * 0.1
from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

playback.play(data)
