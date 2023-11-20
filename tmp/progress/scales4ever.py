from musical.theory import Note, Scale, Chord
from musical.audio import playback

from timeline import Hit, Timeline

import pprint, random
pp = pprint.PrettyPrinter(indent=4)


# TODO
# add in more notes?
    # for j, _note in enumerate(chord):
# sin/cos on the duration and offset wobbles?
# keep track of good durations/offsets as a standard set
    # pick specific note/scale/interval combinations


# Define key and scale
#key = Note('C')
#scale = Scale(key, 'major')

key = Note(random.choice(Note.NOTES))
scales = ['major', 'pentatonicmajor', 'augmented', 'diminished', 'chromatic', 'wholehalf', 'halfwhole', 'wholetone', 'augmentedfifth', 'japanese', 'oriental', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']

scale = Scale(key, random.choice(scales))
progression = Chord.progression(scale, base_octave=key.octave)
chord = progression[0].invert_down()

all_notes = []
for chord in progression:
    all_notes.append(chord.notes[0])
    all_notes.append(chord.notes[1])
    all_notes.append(chord.notes[2])
pp.pprint(all_notes)

time = 0.0 # Keep track of currect note placement time in seconds
timeline = Timeline()

notes = [0,1,2]
random.shuffle(notes)
random.shuffle(all_notes)

for i in range(15):
    interval = 0.1
    offset = 0.6
    pp.pprint([key, scale, chord, progression, notes, interval])

    for j, n in enumerate(all_notes):
        timeline.add(time + interval * j, Hit(n, 0.1))
        #timeline.add(time + interval * j, Hit(chord.notes[n], 0.1))
        
        if(j < 13):
            o_interval = interval + offset
            timeline.add(time + o_interval * 1, Hit(n, 0.025))
            #timeline.add(time + o_interval * 1, Hit(chord.notes[n], 0.05))
    
        time += 0.1

        # TODO update this using noise/cos/sin
        if(interval > 0.5):
            interval -= 0.1
        elif(interval < 0.0):
            interval += 0.1
        else:
            interval = 0.1
        

    #pp.pprint([key, scale, chord, progression, notes, interval])
    
    """
    timeline.add(time + interval * 1, Hit(chord.notes[2].transpose(0), 8.0))
    timeline.add(time + interval * 2, Hit(chord.notes[1].transpose(0), 8.0))
    timeline.add(time + interval * 3, Hit(chord.notes[0].transpose(0), 8.0))
    timeline.add(time + interval * 4, Hit(chord.notes[2], 8.0))
    timeline.add(time + interval * 5, Hit(chord.notes[1], 8.0))
    timeline.add(time + interval * 6, Hit(chord.notes[0], 8.0))

    o_interval = interval + offset
    timeline.add(time + o_interval * 1, Hit(chord.notes[2].transpose(0), 8.0))
    timeline.add(time + o_interval * 2, Hit(chord.notes[1].transpose(0), 8.0))
    timeline.add(time + o_interval * 3, Hit(chord.notes[0].transpose(0), 8.0))

    time += 2.2
    interval += 0.025
    """
    if( i % 5 == 0 and i > 0):
        chord = progression[ random.choice([0,1,2]) ]

    if(i % 10 == 0 and i > 0):
        scale = Scale(key, random.choice(scales))
        progression = Chord.progression(scale, base_octave=key.octave)
        chord = chord.invert_down()

        all_notes = []
        for chord in progression:
            all_notes.append(chord.notes[0])
            all_notes.append(chord.notes[1])
            all_notes.append(chord.notes[2])
        random.shuffle(all_notes)

    if(i % 20 == 0 and i > 0):
        timeline.add(time + 0.02, Hit(chord.notes[0].transpose(0), 4.0))
        timeline.add(time + 0.04, Hit(chord.notes[1].transpose(-6), 4.0))
        timeline.add(time + 0.06, Hit(chord.notes[2].transpose(-12), 4.0))
        time += 3.0

print("Rendering audio...")
data.append(timeline.render())

# Reduce volume to 25%
data[0] = data[0] * 0.25

print("Playing audio...")
playback.play(data[0])