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
iterations = random.randint(12, 36)
duration = 4.0
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
key_note = Note((random.choice(Note.NOTES), random.choice([2]))).note
key = Note(key_note)

scales = ['chromatic', 'major', 'pentatonicmajor', 'mixolydian']
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 1)
pp.pprint(key)
pp.pprint(r_scale)

time += random.randint(2, 8)

for i in range(iterations):
  if i % 4 == 0:
    i_notes = notes[::-2]
  else:
    i_notes = notes[::3]

  for j, note in enumerate(i_notes):
    if j % 3 == 0:
      timeline.add(time + eighth_note, Hit(Note(note).shift_down_octave(1), duration*2))
    else:
      timeline.add(time, Hit(Note(note).shift_down_octave(1), duration*2))
    timeline.add(time + eighth_note + quarter_note, Hit(Note(note).shift_down_octave(1), duration))
  time += sixteenth_note
  timeline.add(time + 0.02, Hit(Note(notes[2]).shift_down_octave(1), duration))

  time += duration * 2
  random.shuffle(notes)
time += duration * 2
  
print("Rendering audio...")
data = timeline.render()

#data = effect.simple_delay(data, 250, 0.98, 1.77)
#data = effect.shimmer(data, 0.234)
data = effect.reverb(data, 0.8, 0.525)
data = effect.echo(data)
data = effect.simple_delay(data, 128, 0.09, 0.77)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)
