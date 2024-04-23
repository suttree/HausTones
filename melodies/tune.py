import os, math
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random
pp = pprint.PrettyPrinter(indent=4)

key_note = Note((random.choice(Note.NOTES), random.choice([0, 1, 2, 3, 4]))).note
key = Note(key_note)
scales = ['major', 'pentatonicmajor', 'japanese', 'locrian', 'ionian', 'mixolydian', 'phrygian']
r_scale = random.choice(scales)
scale = Scale(key, r_scale)
notes = notes_from_scale(key.note, scale.intervals, 2)
notes_with_intervals = add_intervals_to_notes(notes)

time = 0.0
localtime = time

measure_duration = 16.00
duration = 4.0
whole_note = duration
half_note = duration/2
quarter_note = duration/4
eighth_note = duration/8
sixteenth_note = duration/16

timeline = Timeline()
notes = notes_from_scale(key.note, scale.intervals)
notesi = add_intervals_to_notes(notes)

for j in range(4):
  timeline.add(time, Hit(Note(notes[j]), duration))
  timeline.add(time + sixteenth_note, Hit(Note(notes[2]), duration))
  timeline.add(time + eighth_note, Hit(Note(notes[-2]), duration))
  timeline.add(time + eighth_note, Hit(Note(notes[-4]), duration))
  timeline.add(time + sixteenth_note, Hit(Note(notes[2]), duration))
  timeline.add(time + eighth_note, Hit(Note(notes[2]), duration))
  
  time += duration * 2

  timeline.add(time + eighth_note, Hit(Note(notesi[0][0]), notesi[0][1]))
  timeline.add(time + eighth_note, Hit(Note(notesi[0][0]), notesi[0][1]))
  timeline.add(time + sixteenth_note, Hit(Note(notesi[2][0]), notesi[0][1]))
  timeline.add(time + sixteenth_note, Hit(Note(notesi[2][0]), notesi[0][1]))

  time += duration
  
  timeline.add(time + sixteenth_note, Hit(Note(notes[2]), duration))
  timeline.add(time + sixteenth_note, Hit(Note(notes[2]), duration))
  
  timeline.add(time + sixteenth_note, Hit(Note(notes[0]), duration))
  timeline.add(time + eighth_note, Hit(Note(notes[0]), duration))
  
  timeline.add(time + eighth_note, Hit(Note(notes[2]), duration))  
  timeline.add(time + sixteenth_note, Hit(Note(notes[2]), duration))  
  
  timeline.add(time + sixteenth_note, Hit(Note(notes[4]), duration))  
  timeline.add(time + sixteenth_note, Hit(Note(notes[4]), duration))  

  time += duration * 2

data = timeline.render()

#data = data * 0.1
#from musical.utils import save_normalized_audio
#save_normalized_audio(data, 44100, os.path.basename(__file__))

playback.play(data)