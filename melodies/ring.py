from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline

from musical.utils import notes_from_scale

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
duration = 3.147 * random.randint(2, 4)
timeline = Timeline()

# Define key and scale
key = Note(random.choice(['F4', 'Bb', 'C4', 'E']))
scales = ['pentatonicmajor', 'mixolydian', 'phrygian', 'japanese', 'pentatonicminor', 'pentatonicmajor']
random.shuffle(scales)
scale = Scale(key, scales[0])
notes = notes_from_scale(key.note, scale.intervals)

for note in notes:
    timeline.add(time, Hit(Note(note), duration * 4))
    #timeline.add(time, Hit(Note(note).transpose(2), duration * 6))
    timeline.add(time, Hit(Note(note).shift_down_octave(2), duration * 8))

    time += duration

print("Rendering audio...")
data = timeline.render()

#data = effect.chorus(data, 0.175)
#data = effect.feedback_modulated_delay(data, data, 0.36, 0.64)
data = effect.modulated_delay(data, data, 0.214, 0.627)
#data = effect.tremolo(data, 0.2)
data = effect.flanger(data, 0.027)

# Reduce volume
#data = data * 0.10

print("Playing audio...")
playback.play(data)