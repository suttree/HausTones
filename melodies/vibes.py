# Je n'est vivre

# To keep: oudh, pppony, Bb-asc/desc, slow
# To run: venv/bin/python3.12 melodies/stepping.py

# todo: use Ara melodies?
# todo: more notes in notes_from_scale
# todo: add interval to notes should pass a param that starts at 0.0 and increases (0.1, 0.2) etc, incl option to add noise to the increments)

# TODO: test the asc and desc parts individually, get them working
# TODO: export to wav for playback later

import os
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = 5
duration = 4.0
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([0, 1, 2, 3]))).note
key = Note(key_note)

#scales = ['chromatic']
scales = ['major', 'pentatonicmajor', 'japanese', 'diminished', 'locrian', 'ionian', 'mixolydian', 'phrygian']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
notes_with_intervals = add_intervals_to_notes(notes)
pp.pprint(key)
pp.pprint(r_scale)

# Descending arppegio
for i in range(7):
  for j, note in enumerate(notes[::-1]):
      pp.pprint(note)
      timeline.add(time + 0.25 * j*i, Hit(Note(note), duration))
      for x in range(7):
        timeline.add(time + 0.25 * j*i*x, Hit(Note(note), duration/2))
  #duration += 0.5
  time += 0.5

print("Rendering audio...")
data = timeline.render()

print("Playing audio...")
#playback.play(data)

#data = data * 0.5
import wave
import numpy as np
from datetime import datetime

now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")

current_script_filename = os.path.basename(__file__)

# mono
output_file = f"{current_script_filename}_output_mono_{timestamp}.wav"
sample_rate = 44100
with wave.open(output_file, 'wb') as wav_file:
    wav_file.setnchannels(1)  # Mono audio
    wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(playback.encode.as_int16(data).tobytes())

# stereo
output_file = f"output_stereo_{timestamp}.wav"
sample_rate = 44100
stereo_data = np.repeat(data[:, np.newaxis], 2, axis=1)
with wave.open(output_file, 'wb') as wav_file:
    wav_file.setnchannels(2)  # Stereo audio
    wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(playback.encode.as_int16(stereo_data).tobytes())

print(f"Audio exported as {output_file}")