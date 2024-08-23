# Je n'est vivre

import os
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random, math

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
offset = 0.4286
iterations = random.randint(4, 18)
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([1, 2, 3]))).note
key = Note(key_note)

scales = ['major', 'pentatonicmajor', 'japanese', 'diminished', 'locrian', 'ionian', 'mixolydian', 'phrygian']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 3)
notes_with_intervals = add_intervals_to_notes(notes)
pp.pprint(key)
pp.pprint(r_scale)

duration = 4.286 # 140bpm
measure_duration = duration * 4
half_measure = measure_duration/2
whole_note = duration
three_quarter_note = duration * 0.75
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

def play_chord(notes, duration):
  timeline.add(time, Hit(Note(notes[0]), duration))

  timeline.add(time, Hit(Note(notes[2]), duration))
  timeline.add(time, Hit(Note(notes[2]).shift_down_octave(2), duration))

  timeline.add(time, Hit(Note(notes[3]), duration))

def reset():
  key_note = Note((random.choice(Note.NOTES), random.choice([2,3]))).note
  key = Note(key_note)
  r_scale = random.choice(scales)
  scale = Scale(key, r_scale)
  notes = notes_from_scale(key.note, scale.intervals)
  
time += sixteenth_note + random.uniform(1.5, 3.2)

for i in range(iterations):
  reset()
  for j, note in enumerate(notes[::2]):
    if j == 0:
    timeline.add(time+0.022*j+math.cos(time), Hit(Note(note).shift_down_octave(1), duration + math.sin(time)))
    timeline.add(time+0.022*j+math.sin(time), Hit(Note(note), duration))

  time += half_measure - math.cos(time) * 2

time += sixteenth_note + random.uniform(1.5, 3.2)

print("Rendering audio...")
data = timeline.render(2)
data = effect.shimmer_wobble(data, 0.24)
data = effect.feedback_modulated_delay(data, data * 1.25, 0.5, 0.2)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)