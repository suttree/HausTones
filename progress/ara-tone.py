import os, sys, getopt, datetime
import random

def main(argv):
  global _debug
  _debug = 0

  from musical.theory import Note, Scale, Chord
  from musical.audio import effect, playback

  from timeline import Hit, Timeline

  # Define key and scale
  key = Note((random.choice(Note.NOTES), random.choice([2,3,3])))

  scales = ['major', 'minor', 'melodicminor', 'harmonicminor', 'pentatonicmajor', 'bluesmajor', 'pentatonicminor', 'bluesminor', 'augmented', 'diminished', 'wholehalf', 'halfwhole', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']
  random.shuffle(scales)
  scale = Scale(key, random.choice(scales))

  print(key)
  print(scale)

  # Grab progression chords from scale starting at the octave of our key
  progression = Chord.progression(scale, base_octave=key.octave)

  time = 0.0 # Keep track of correct note placement time in seconds

  timeline = Timeline()

  # Pick a notes from a chord randomly chosen from a list of notes in this progression
  chord = progression[ random.choice(range(len(progression)-1)) ]
  notes = chord.notes

  # Testing a new melody-generation idea - duncan 11/4/20
  # - needs more work, disabling for now - 12/4/20
  random_melody = []
  melody_length = random.randrange(1, 12)
  
  for i in range(0, melody_length):
    random_melody.append( round(random.uniform(0.1, 0.6), 1) )

  random_melody = random.choice(melodies)
  print(random_melody)

  last_interval = 0.0
  last_transpose = 0

  for i, interval in enumerate(random_melody):
    random_note = random.choice(notes)

    if i % 3 == 0:
      random_transpose = random.choice([8, 12])
    elif (last_interval == interval):
      if random.choice([0,1,2]) == 2:
        random_transpose = last_transpose
      else:
        random_transpose = 0
    else:
      random_transpose = random.choice([0,2,4,6,8,10,12])

    last_interval = interval
    last_transpose = random_transpose

    note = random_note.transpose(random_transpose)
    
    # favour queued notes, but occasionally overlap them too
    if (random.choice([1,2,3,4,5,6]) > 2):
      time = time + interval
      timeline.add(time, Hit(note, interval))
    else:
      timeline.add(time, Hit(note, interval))
      time = time + interval

  data = timeline.render()

  # Reduce volume to 50%
  data = data * 0.5

  print("Playing audio...")
  for i in range(random.choice([1,2])):
    playback.play(data)

if __name__ == "__main__":
  main(sys.argv[1:])

