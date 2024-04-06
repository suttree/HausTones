from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, add_intervals_to_notes
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = 5
duration = 4.0
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([1,2,3,4,5]))).note
key = Note(key_note)

#scales = ['pentatonicmajor', 'mixolydian', 'phrygian', 'japanese', 'pentatonicminor', 'pentatonicmajor']
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
for i, note in enumerate(notes_with_intervals):
    timeline.add(time, Hit(Note(note[0]), duration))
time += duration

for i in range(60):
    for j, note in enumerate(notes_with_intervals):
        timeline.add(time + note[1], Hit(Note(note[0]), duration))
        
    #if j % 20 == 0:
    #    for note in enumerate(notes_with_intervals):
    #        timeline.add(time, Hit(Note(note[0]), duration))

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
data = effect.tremolo(data, freq=0.22)
data = effect.chorus(data, 0.75)

print("Playing audio...")
playback.play(data)