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
iterations = random.randint(8, 28)
duration = 4.0
timeline = Timeline()

measure_duration = 22.00
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

scales = ['ionian', 'phrygian', 'ionian', 'augmentedfifth', 'melodicminor']
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
pp.pprint(key)
pp.pprint(r_scale)

def play_chord(notes, duration):
  timeline.add(time, Hit(Note(notes[0]), duration))
  timeline.add(time, Hit(Note(notes[2]).shift_down_octave(2), duration))
  timeline.add(time, Hit(Note(notes[3]), duration))
  timeline.add(time, Hit(Note(notes[5]), duration))

for i in range(iterations):
  random.shuffle(notes)
  for j, note in enumerate(notes[::-4]):
    timeline.add(time + eighth_note, Hit(Note(note), duration))
    time += 0.1
  time += half_note
  
  timeline.add(time + eighth_note, Hit(Note(notes[0]), duration*2))
  timeline.add(time + eighth_note + half_note, Hit(Note(notes[2]), duration*2))
  
  time += half_note
  
  play_chord(notes, measure_duration*2)
  
  time += duration * 2

time += measure_duration

notes = extended_notes_from_scale(key.note, scale.intervals, 2)
for j, note in enumerate(notes[::-4]):
  timeline.add(time + eighth_note, Hit(Note(note), duration))
  time += 0.1
  
print("Rendering audio...")
data = timeline.render()

data = effect.shimmer_wobble(data, 0.34)
data = effect.feedback_modulated_delay(data, data * 1.25, 0.5, 0.2)
data = effect.simple_delay(data, 256, 0.49, 0.77)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)
