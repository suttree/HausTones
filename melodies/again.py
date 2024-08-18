from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, add_intervals_to_notes
import pprint, random
import numpy as np
import os, math

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = random.randint(4, 10)
duration = 4.2

# Define key and scale
key = Note('C4')

scales = ['ionian', 'major']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = notes_from_scale(key.note, scale.intervals)
notesi = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(r_scale)
pp.pprint(scale)
pp.pprint(notes)

time = 0.0
localtime = time

measure_duration = 16.00
duration = 4.0
whole_note = duration
three_quarter_note = duration * 0.75
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

timeline = Timeline()

time += 0.38 + random.uniform(0.8, 4.3)

# Create a separate timeline for each note
for i, note in enumerate(notes):
    time += half_note
    timeline.add(time, Hit(Note(note), three_quarter_note))

    if i % 2 == 0 and i > 0:
      for i, note in enumerate(notes[4::-1]):
          time += quarter_note
          timeline.add(time, Hit(Note(note), three_quarter_note))

    if i % 3 == 0 and i > 0:
      random.shuffle(notes)

time += half_note

for i in range(iterations):
  timeline.add(time + whole_note, Hit(Note(notesi[0][1]), duration))
  
  top = random.choice([1,2,4])
  timeline.add(time + whole_note, Hit(Note(notes[top]), duration))

  time += 0.1
  timeline.add(time + quarter_note, Hit(Note(notes[0]), duration))

  time += 0.45 * math.sin(i)
  top = random.choice([0,3])
  timeline.add(time + whole_note, Hit(Note(notes[top]), duration))

  time += whole_note
  
time += 0.38 + random.uniform(0.8, 4.3)

print("Rendering audio...")
data = timeline.render()
data = effect.tremolo(data, freq=7.7)
data = effect.simple_delay(data)
data = effect.reverb(data)
data = effect.echo(data)
data = effect.shimmer_wobble(data)
#data = effect.volume_swell(data, swell_duration=1.25)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)