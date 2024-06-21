# Je n'est vivre

import os, math
from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
from musical.utils import notes_from_scale, extended_notes_from_scale, add_intervals_to_notes, add_random_float
import pprint, random

pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0  # Keep track of current note placement time in seconds
offset = 0.0
iterations = random.randint(12, 46)
duration = 36.0
increment = math.sin(0.19750)
timeline = Timeline()

# Define key and scale
key_note = Note((random.choice(Note.NOTES), random.choice([0]))).note
key = Note(key_note)

scales = ['japanese', 'major', 'ionian', 'mixolydian', 'phrygian', 'major', 'japanese', 'ionian', 'augmented', 'augmentedfifth', 'melodicminor']

r_scale = random.choice(scales)
scale = Scale(key, r_scale)
#notes = notes_from_scale(key.note, scale.intervals)
notes = notes_from_scale(key.note, scale.intervals)
notes = extended_notes_from_scale(key.note, scale.intervals, 1)
notes_with_intervals = add_intervals_to_notes(notes)

pp.pprint(key)
pp.pprint(r_scale)

# arppegio to open
#for i in range(1):
#  for i in range(2z):
#    localtime = time
#    for j, note in enumerate(notes[::2]):
#        timeline.add(localtime + 2.47, Hit(Note(note), duration))
#        localtime += increment
#    for j, note in enumerate(notes[5::]):
#        timeline.add(localtime + 3.42, Hit(Note(note), duration))
#        localtime += increment * math.sin(i)
#    locatime = time
#    time += duration

#  key_note = Note((random.choice(Note.NOTES), random.choice([1, 2]))).note
#  key = Note(key_note)
#  notes = notes_from_scale(key.note, scale.intervals)
#  notes_with_intervals = add_intervals_to_notes(notes)
#
#  for i in range(4):
#    localtime = time
#    for j, note in enumerate(notes):
#        timeline.add(time + 1.46, Hit(Note(notes[0]), duration/2))
#    for j, note in enumerate(notes[::2]):
#        timeline.add(localtime + 3.41, Hit(Note(note), duration))
#        localtime += increment
#    for j, note in enumerate(notes[::5]):
#        timeline.add(localtime + 2.44, Hit(Note(note), duration))
#        localtime += increment * math.sin(i)
#    locatime = time
#    time += duration
#    
#  key_note = Note((random.choice(Note.NOTES), random.choice([1, 2]))).note
#  key = Note(key_note)
#  notes = notes_from_scale(key.note, scale.intervals)
#  notes_with_intervals = add_intervals_to_notes(notes)

def play_triad(time):
  timeline.add(time + 0.0042 + math.sin(increment), Hit(Note(notes[0]), duration))
  timeline.add(time + 0.0042 + math.sin(increment), Hit(Note(notes[3]), duration))
  timeline.add(time + 0.0042 + math.sin(increment), Hit(Note(notes[5]), duration))
      
def strum_chord(time):
  for j, note in enumerate(notes):
      timeline.add(time + 0.0035 * j + math.sin(increment), Hit(Note(note), duration))

def play_chord(notes, duration):
  timeline.add(time, Hit((Note(notes[0])), duration))
  timeline.add(time, Hit(Note(notes[0]), duration))
  timeline.add(time + 0.02, Hit(Note(notes[0]), duration))
  
for i in range(iterations):
  strum_chord(time)
  time += duration/16
  play_triad(time)
  time += duration/16 + math.cos(increment) * math.sin(increment)

#for i in range(4):
#  duration += math.cos(i)
#  for j, note in enumerate(notes_with_intervals):
#      timeline.add(time + increment, Hit(Note(note[0]), duration/4))
#      #interval = math.cos(increment) * math.sin(increment)
#      timeline.add(time + increment, Hit(Note(note[0]), duration/8))
#
#  time += duration/4
#  increment -= math.cos(increment)



## Ascending arpeggio to open
#for j, note in enumerate(notes):
#    timeline.add(time + 0.40 * j + math.sin(increment), Hit(Note(note), duration))
#for j, note in enumerate(notes[::2]):
#    timeline.add(time + 0.40 * j + math.cos(increment), Hit(Note(note), duration))
#time += duration + increment
#increment += math.sin(increment)
#    
#for i in range(80):
#    for j, note in enumerate(notes_with_intervals):
#        interval = add_random_float(note[1], math.cos(increment), math.sin(increment))
#        timeline.add(time + interval, Hit(Note(note[0]), note[1]))
#    time += duration
#    increment -= math.sin(increment)
#    
#r_scale = random.choice(scales)
#scale = Scale(key, r_scale)
#notes = notes_from_scale(key.note, scale.intervals)
#notes_with_intervals = add_intervals_to_notes(notes)
#
## And breathe....
#time += duration * 2.2
#
#for i in range(30):
#    for j, note in enumerate(notes_with_intervals):
#        interval = add_random_float(note[1], -math.cos(increment), math.sin(increment))
#        timeline.add(time + interval, Hit(Note(note[0]), duration))
#        timeline.add(time + increment, Hit(Note(note[0]), duration))
#    time += duration
#    increment -= math.cos(increment)
#
## And breathe....
#time += duration * 2.4

print("Rendering audio...")
data = timeline.render()
#data = effect.shimmer(data, 0.324)
#data = effect.tremolo(data, freq=0.64)
data = effect.reverb(data, 0.28, 0.525)
data = effect.echo(data)
#data = effect.simple_delay(data)
#data = effect.pitch_shift(data, 2)

data = data * 0.25

#from musical.utils import save_normalized_audio
#save_normalized_audio(data, 44100, os.path.basename(__file__))

playback.play(data)
