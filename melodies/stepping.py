from musical.theory import Note, Scale, Chord
from musical.audio import playback, effect

from musical.utils import notes_from_scale

from timeline import Hit, Timeline

import pprint, random, math, time
pp = pprint.PrettyPrinter(indent=4)

# Config vars
stime = 0.0 # Keep track of currect note placement stime in seconds
timeline = Timeline()

interval = 0.1      # gap between notes
interval = random.uniform(0.1, 1.2)
offset = 0.2        # offset applied each loop
offset = interval + random.uniform(0.1, 0.7)
iterations = 48     # number of times to loop
iterations = random.randint(6, 22)

pp.pprint(interval)
pp.pprint(offset)
pp.pprint(iterations)
pp.pprint('----')

# Define key and scale
key = Note(random.choice(Note.NOTES))
scale = Scale(key, 'chromatic')
notes = notes_from_scale(key.note, scale.intervals)

if(random.randint(1, 10) % 2 == 0):
    pp.pprint('descending')
    notes = notes[::-1]         # descending
    #random.shuffle(notes)       # random

pp.pprint('chromatic..')
pp.pprint(scale)
pp.pprint(key)
pp.pprint(notes)
pp.pprint('--setup--')

for i in range(iterations):
    base_time = stime
    for note in notes:
        note = Note(note)

        timeline.add(stime, Hit(note, 3.14))
        stime += interval

    stime = base_time
    for note in notes:
        note = Note(note)

        timeline.add(stime, Hit(note, 3.14))
        stime += offset
        
    stime = base_time
    for note in notes:
        note = Note(note)

        timeline.add(stime, Hit(note, 3.14))
        stime += interval + offset

    
    if(i % 6 == 0 and i > 0):
        timeline.add(stime + interval, Hit(note.shift_down_octave(2), 8.0))
        timeline.add(stime + interval, Hit(note.shift_down_octave(1), 7.0))
        timeline.add(stime + interval, Hit(note.shift_down_octave(1), 6.0))


    if(i % 12 == 0 and i > 0):
        timeline.add(stime + 0.1, Hit(note.shift_down_octave(1), 6.0))
        timeline.add(stime + 0.2, Hit(note.shift_down_octave(1), 7.0))
        timeline.add(stime + 0.3, Hit(note.shift_down_octave(2), 8.0))

    if(i % 24 == 0 and i > 0):
        interval += 0.012
        offset += 0.017

    if(i % 36 == 0 and i > 0):
        interval -= 0.021
        offset -= 0.013
        
    if(i % 44 == 0 and i > 0):
        pp.pprint('rewinzd')
        stime -= 3.14

    if(interval <= 0.0):
        interval = 0.4286

    if(offset <= 0.0):
        offset = 0.6824

print("Rendering audio...")
data = timeline.render()

# Reduce volume to 25%
data = data * 0.25

#switch = int(min(max(stime * (1 - math.cos(time.time())), 1), 5))
#switch = stime * math.cos(time.time())
#switch = random.randint(1, 49)
#pp.pprint(switch)

#if(switch % 6 == 0):
#    pp.pprint('tremelo...')
#    data = effect.tremolo(data, 0.24)

#if(switch % 5 == 0):
#    pp.pprint('feedback delay...')
#    data = effect.feedback_modulated_delay(data, data, 0.036, 0.64)

#if(switch % 3 == 0):
#    pp.pprint('delaying...')
#    data = effect.modulated_delay(data, data, 0.024, 0.26)

#if(switch % 2 == 0):
#    pp.pprint('flanger...')
#    data = effect.flanger(data, 0.026)

print("Playing audio...")
playback.play(data)