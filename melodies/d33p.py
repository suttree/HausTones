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
import wave
import numpy as np
from datetime import datetime

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = 5
duration = 2.24
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([1, 2]))).note
key = Note(key_note)

#scales = ['chromatic']
scales = ['major', 'pentatonicmajor', 'japanese', 'diminished', 'locrian', 'ionian', 'mixolydian', 'phrygian']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = extended_notes_from_scale(key.note, scale.intervals, 2)
notes_with_intervals = add_intervals_to_notes(notes)
#pp.pprint(key)
#pp.pprint(r_scale)

# Descending arppegio
for x in range(1):
  #pp.pprint(x)
  for i in range(16):
    for j, note in enumerate(notes[::-1]):
        #pp.pprint(note)
        inc = 0.025 * j * i
        #if inc > 4.0: inc = add_random_float(4.0, -0.4, 0.4)
        timeline.add(time + inc, Hit(Note(note), duration + inc))
        #pp.pprint(inc)

    duration += 0.276 # or inc?
    time += duration

print("Rendering audio...")
data = timeline.render()

# Normalize audio data
max_amplitude = np.max(np.abs(data))
scaling_factor = 1.0 / max_amplitude
normalized_data = data * scaling_factor

# Apply effects
normalized_data = effect.tremolo(normalized_data, freq=1.7)
normalized_data = effect.modulated_delay(normalized_data, normalized_data, 0.02, 0.003)
normalized_data = effect.reverb(normalized_data, 0.8, 0.425)

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
    wav_file.writeframes(playback.encode.as_int16(normalized_data).tobytes())

print(f"Audio exported as {output_file}")