from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline

from musical.utils import notes_from_scale

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0
offset = random.uniform(10.8, 24.2)
iterations = random.randint(8, 42)
duration = random.uniform(8.7, 12.6)
nudge_x = random.uniform(0.002, 0.026)
nudge_y = random.uniform(0.001, 0.028)

# Define key and scale
key = Note(random.choice(Note.NOTES))
scales = ['major', 'pentatonicmajor', 'augmented', 'diminished', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']
scale = Scale(key, random.choice(scales))
notes = notes_from_scale(key.note, scale.intervals)
progression = Chord.progression(scale, base_octave=key.octave)

roll = random.randint(1,6)
if (roll == 2):
    notes.reverse()
elif (roll == 4):
    random.shuffle(notes)

timeline = Timeline()
for i in range(iterations):
    for j, note in enumerate(notes):
        timeline.add(time + offset * j, Hit(Note(note), duration))
        offset += nudge_x
    time += duration

    offset -= nudge_x * len(notes)
    duration -= nudge_y * len(notes)

print("Rendering audio...")
data = timeline.render()
data = effect.flanger(data, 0.026)

# Reduce volume to 25%
#data = data * 0.25

print("Playing audio...")
playback.play(data)