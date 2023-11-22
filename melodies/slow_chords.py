from musical.theory import Note, Scale, Chord
from musical.audio import effect, playback
from timeline import Hit, Timeline
import pprint, random
pp = pprint.PrettyPrinter(indent=4)

# Config vars
time = 0.0 # Keep track of currect note placement time in seconds
timeline = Timeline()
interval = random.uniform(0.2, 0.6)
offset = interval + random.uniform(0.1, 0.3)
offset_i = 0.0
iterations = random.randint(6, 22)
duration = random.uniform(1.0, 8.0)

def notes_from_scale(starting_note, intervals):
    #pp.pprint(starting_note[0])
    starting_note = starting_note[0]
    # Initialize a list to store the notes
    scale = [starting_note]

    # Calculate the notes in the scale
    current_note = starting_note
    for interval in intervals:
        # Calculate the next note by adding the interval to the current note
        next_note_index = (ord(current_note) - ord('A') + interval) % 7
        next_note = chr(ord('A') + next_note_index)
        
        # Append the next note to the scale
        scale.append(next_note)
        
        # Update the current note for the next iteration
        current_note = next_note

    return scale

# Define key and scale
key = Note(random.choice(Note.NOTES))
scale = Scale(key, 'chromatic')
notes = notes_from_scale(key.note, scale.intervals)
progression = Chord.progression(scale)
chord = progression[0]

for i in range(iterations):
    for j, note in enumerate(notes[::-1]):
        note = Note(note)
        timeline.add(time + offset_i * j, Hit(note, duration))

    time += 1.0 # random.uniform(1.0, 2.0) #1.25
    offset_i 0.5 # += random.uniform(0.1, 0.2) #0.125

#print "Rendering audio..."
data = timeline.render()

data = effect.chorus(data, 0.1)

# Reduce volume to 10%
data = data * 0.10

#print "Playing audio..."
playback.play(data)