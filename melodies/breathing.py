# KISAS - keep it slow & simple

from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline

from musical.utils import notes_from_scale

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0
offset = 12.4286
iterations = random.randint(8, 42)
duration = 8.286

# Define key and scale
key = Note(random.choice(Note.NOTES))
scales = ['major', 'pentatonicmajor', 'augmented', 'diminished', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']
scale = Scale(key, random.choice(scales))
notes = notes_from_scale(key.note, scale.intervals)
progression = Chord.progression(scale, base_octave=key.octave)

roll = random.randint(1,6)
if (roll == 3):
    notes.reverse()
elif (roll == 6):
    random.shuffle(notes)

timeline = Timeline()
for i in range(iterations):
    for j, note in enumerate(notes):
        timeline.add(time + offset * j, Hit(Note(note), duration))
    time += duration

    if (i % 33) == 0:
       time -= 0.42 

print("Rendering audio...")
data = timeline.render()
data = effect.flanger(data, 0.016)
data = effect.feedback_modulated_delay(data, data, 0.036, 0.64)

# Reduce volume to 25%
#data = data * 0.25

print("Playing audio...")
playback.play(data)