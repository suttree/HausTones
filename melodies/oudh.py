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
key_note = Note((random.choice(Note.NOTES), random.choice([0,1,2,3,4,5,6,7,8,9,10,11]))).note
key = Note(key_note)

scales = ['major', 'pentatonicmajor', 'augmented', 'diminished', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']
random.shuffle(scales)
scale = Scale(key, scales[0])
notes = notes_from_scale(key.note, scale.intervals)
notes_with_intervals = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(scale)
pp.pprint(notes)
pp.pprint(notes_with_intervals)

# Start with all notes on 0
#for i, note in enumerate(notes_with_intervals):
#    timeline.add(time, Hit(Note(note[0]), duration))
#time += duration

# Now play each note staggered
# todo: pan effect
# todo: different 'pluck' effect
# todo: more notes in notes_from_scale
#for i, note in enumerate(notes_with_intervals):
#    timeline.add(time, Hit(Note(note[0]), duration))
#time += duration

for i in range(25):
    for j, note in enumerate(notes_with_intervals):
        interval = add_random_float(note[1], -1.25, 0.75)
        timeline.add(time + interval, Hit(Note(note[0]), duration/2))
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
data = effect.tremolo(data, freq=4.92)
#data = effect.chorus(data, 0.75)
#data = effect.pan(data, len(data) / 44100, 44100, pan_freq=0.2)
data = effect.feedback_modulated_delay(data, data, 2.26, 0.44)
#data = effect.modulated_delay(data, data, 0.2, 1.6)
#data = effect.flanger(data, 0.4)


print("Playing audio...")
playback.play(data)