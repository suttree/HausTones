import os, math
import time as thetime
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = random.randint(18, 72)
duration = 4.0
increment = random.uniform(0.025, 0.64) + math.cos(thetime.time()) * math.sin(0.19750)
timeline = Timeline()

measure_duration = 14.00
half_measure = measure_duration/2
duration = measure_duration/4
whole_note = duration
three_quarter_note = duration * 0.75
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([1]))).note
key = Note('e4')

scales = ['japanese', 'major', 'ionian', 'mixolydian', 'phrygian', 'ionian', 'augmentedfifth', 'melodicminor']
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 1)
notes_with_intervals = add_intervals_to_notes(notes)
pp.pprint(key)
pp.pprint(r_scale)

def play_chord(notes, duration, time):
  timeline.add(time, Hit(Note(notes[0]), duration))
  timeline.add(time, Hit(Note(notes[2]).shift_down_octave(2), duration))
  timeline.add(time, Hit(Note(notes[3]), duration))
  timeline.add(time, Hit(Note(notes[5]), duration))

time += sixteenth_note + random.uniform(0.8, 2.4)

for i in range(iterations):
  play_chord(notes, measure_duration*2, time)
  if (i % 3 == 0 and i > 0):
    random.shuffle(notes)
    play_chord(notes, measure_duration, time)
  time += half_measure + math.cos(thetime.time())
time += sixteenth_note * math.cos(thetime.time())

print("Rendering audio...")
data = timeline.render()

data = effect.shimmer_wobble(data, 0.34)
data = effect.feedback_modulated_delay(data, data * 0.25, 0.05, 0.02)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)
