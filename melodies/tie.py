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
iterations = random.randint(12, 52)
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
key_note = Note((random.choice(Note.NOTES), random.choice([1]))).note
key = Note('c4')

scales = ['major', 'pentatonicmajor', 'japanese', 'locrian', 'ionian', 'mixolydian', 'phrygian']
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 1)
pp.pprint(key)
pp.pprint(r_scale)

def reset():
  key_note = Note((random.choice(Note.NOTES), random.choice([2,3]))).note
  key = Note(key_note)
  r_scale = random.choice(scales)
  scale = Scale(key, r_scale)
  notes = notes_from_scale(key.note, scale.intervals)
  progression = Chord.progression(scale)
  chord = progression[0]

def play_chord(notes, duration):
  timeline.add(time, Hit(Note(notes[0]), duration))
  #timeline.add(time + 0.05, Hit(Note(notes[0]), duration))

  timeline.add(time, Hit(Note(notes[2]), duration))
  timeline.add(time, Hit(Note(notes[2]).shift_down_octave(2), duration))
  #timeline.add(time + 0.05, Hit(Note(notes[2]).shift_down_octave(2), duration))

  timeline.add(time, Hit(Note(notes[3]), duration))
  #timeline.add(time + 0.05, Hit(Note(notes[3]), duration))

arp = [0,1,2,3,4]
time += sixteenth_note + random.uniform(1.5, 3.2)

for i in range(iterations):

  timeline.add(time + eighth_note, Hit(Note(notes[ arp[0] ]), duration*2))
  timeline.add(time + eighth_note + half_note + math.sin(time), Hit(Note(notes[ arp[2] ]), duration*2))
  
  time += whole_note
  play_chord(notes, measure_duration)

  random.shuffle(arp)

  if i % 3 == 0 and i > 0:
    reset()

  time += duration + math.cos(time)
time += measure_duration * 2

time += sixteenth_note + random.uniform(1.5, 2.2)

print("Rendering audio...")
data = timeline.render()

#data = effect.reverb(data, 0.8, 0.525)

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)
