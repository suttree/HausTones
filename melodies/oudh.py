# To keep: oudh, pppony, Bb-asc/desc, slow
# To run: venv/bin/python3.12 melodies/stepping.py


from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = 5
duration = 4.0
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([0, 1, 2, 3, 4]))).note
key = Note(key_note)

#scales = ['chromatic']
scales = ['major', 'pentatonicmajor', 'augmented', 'diminished', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']
scale = Scale(key, random.choice(scales))
notes = notes_from_scale(key.note, scale.intervals)
notes_with_intervals = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(scale)
pp.pprint(notes)
pp.pprint(notes_with_intervals)

# todo: use Ara melodies?
# todo: more notes in notes_from_scale
# todo: add interval to notes should pass a param that starts at 0.0 and increases (0.1, 0.2) etc, incl option to add noise to the increments)


for i in range(3):
    for j, note in enumerate(notes_with_intervals):
        interval = add_random_float(note[1], -1.25, 2.75)
        timeline.add(time + interval, Hit(Note(note[0]), duration))
    time += duration


#note = notes_with_intervals[0]
#note2 = notes_with_intervals[1]
#for i in range(3):
#    timeline.add(time + note[1], Hit(Note(note[0]), duration))
#    timeline.add(time + note2[1], Hit(Note(note2[0]), duration))
#    time += duration

#for i in range(2):
#    for j, note in enumerate(notes_with_intervals):
#        timeline.add(time + note[1], Hit(Note(note[0]), duration))
#    time += duration


print("Rendering audio...")
data = timeline.render()
#data = effect.shimmer(data, 2.047)
data = effect.shimmer_wobble(data)
#data = effect.tremolo(data, freq=1.1)
#data = effect.pan(data, len(data) / 44100, 44100, pan_freq=0.2)
#data = effect.feedback_modulated_delay(data, data, 1.26, 1.44)
#data = effect.feedback_modulated_delay(data, data, 0.036, 0.64)
#data = effect.modulated_delay(data, data, 0.2, 1.8)
#data = effect.flanger(data, 0.4)
#data = effect.chorus(data, 0.45)
#data = effect.reverb(data, 0.8, 0.025)

print("Playing audio...")
playback.play(data)