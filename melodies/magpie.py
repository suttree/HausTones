# Je n'est vivre

import os, math
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random
import wave
import numpy as np
from datetime import datetime

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = 5
duration = 4.0
timeline = Timeline()

# Define key and scale
key_note = random.choice(Note.NOTES) + '2'
key = Note(key_note)
pp.pprint(key)

scales = ['pentatonicminor', 'ionian']
#scales = ['major', 'pentatonicmajor', 'japanese', 'diminished', 'locrian', 'ionian', 'mixolydian', 'phrygian']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 3)
notesi = add_intervals_to_notes(notes)
pp.pprint(key)
pp.pprint(r_scale)

measure_duration = 16.00
half_measure = measure_duration/2
duration = measure_duration/4
whole_note = duration
three_quarter_note = duration * 0.75
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

def play_chord(notes, duration):
  timeline.add(time, Hit(Note(notes[0][0]).shift_down_octave(1), notes[0][1]))
  timeline.add(time, Hit(Note(notes[2][0]).shift_down_octave(1), notes[2][1]))
  timeline.add(time, Hit(Note(notes[4][0]).shift_down_octave(1), notes[4][1]))
  timeline.add(time, Hit(Note(notes[4][0]), notes[4][1]))
  timeline.add(time, Hit(Note(notes[4][0]), notes[4][1]))
  timeline.add(time, Hit(Note(notes[0][0]).shift_down_octave(1), notes[4][1]))


for i in range(6):
    play_chord(notesi, half_note)
    time += sixteenth_note
    play_chord(notesi, half_note)
    time += half_note
    
    for j, note in enumerate(notesi[::-2], 2):
      timeline.add(time, Hit(Note(note[0]), half_note))
      time += notesi[0][1]
      for k, note in enumerate(notesi[::2], 2):
        timeline.add(time, Hit(Note(note[0]), three_quarter_note))
        time += sixteenth_note
    time += eighth_note

print("Rendering audio...")
data = timeline.render()
#data = effect.simple_delay(data, 0.75)
data = effect.octave(data, 0.74)
data = effect.shimmer_wobble(data, 0.74)

data = data * 0.25

from musical.utils import save_normalized_audio
save_normalized_audio(data, 44100, os.path.basename(__file__))

#playback.play(data)
