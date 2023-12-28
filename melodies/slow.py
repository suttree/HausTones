
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale

import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0
offset = 12.4421
iterations = random.randint(1, 2)
duration = 18.28281

# Define key and scale
key = Note(random.choice(Note.NOTES))
scales = ['major', 'pentatonicmajor', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'harmonic major']
scale = Scale(key, random.choice(scales))
notes = notes_from_scale(key.note, scale.intervals)
progression = Chord.progression(scale, base_octave=key.octave)

roll = random.randint(1,6)
if (roll == 1):
    notes.reverse()
elif (roll == 6):
    random.shuffle(notes)

timeline = Timeline()
for i in range(iterations):
    for j, n in enumerate(notes):
        note = Note(n)
        note = note.shift_down_octave(1.5)
        timeline.add(time + offset * j, Hit(Note(note), duration))
    time += duration

    if (iterations - i) < 3:
       time -= 0.71

print("Rendering audio...")
data = timeline.render()
data = effect.feedback_modulated_delay(data, data, 0.6047, 0.83)
data = effect.tremolo(data, 0.052)

# Reduce volume
#data = data * 0.07

print("Playing audio...")
playback.play(data)