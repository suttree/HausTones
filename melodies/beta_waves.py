import os
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from musical.utils import notes_from_scale

from timeline import Hit, Timeline

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
timeline = Timeline()
interval = random.uniform(0.2, 1.6)
offset = interval + random.uniform(0.1, 0.6)
offset_i = 0.0
iterations = random.randint(16, 68)
#iterations = random.randint(16, 16)
duration = random.uniform(1.0, 8.0)

# Define key and scale
#key = Note(random.choice(Note.NOTES))
key = Note('F')
scale = Scale(key, 'chromatic')
notes = notes_from_scale(key.note, scale.intervals)

for i in range(iterations):
    if (i > iterations -8): break # skip the lone notes at the end

    for j, note in enumerate(notes[::-1]):
        note = Note(note)
        timeline.add(time + offset_i * j, Hit(note, duration))
    time += 1.25/2 #random.uniform(0.75, 2.0) #1.25
    offset_i += 0.125 #random.uniform(0.1, 0.275) #0.125
        
print("Rendering audio...")
data = timeline.render()
#data = effect.shimmer(data, 3.147)
data = effect.reverb(data, 0.8, 0.025)
data = effect.tremolo(data, 0.1)

# Reduce volume to 25%
#data = data * 0.25

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
stereo_data = np.repeat(data[:, np.newaxis], 2, axis=1)
sample_rate = 44100
with wave.open(output_file, 'wb') as wav_file:
    wav_file.setnchannels(2)  # Stereo audio
    wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(playback.encode.as_int16(stereo_data).tobytes())

print(f"Audio exported as {output_file}")