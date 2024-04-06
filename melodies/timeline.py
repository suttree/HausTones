from collections import defaultdict

from musical.audio import source

import numpy as np

# XXX: Early implementation of timeline/hit concepts. Needs lots of work

# TODO: Associate sound source with Hit instances somehow
# TODO: Amplitude, possibly other dynamics attributes


#class Hit:
#    '''
#    Rough draft of Hit class. Stores information about the hit and generates
#    the audio array accordingly. Currently implements a basic cache to avoid
#    having to rerender identical hits
#    '''
#    cache = {}
#
#    def __init__(self, note, duration):
#        self.note = note
#        self.duration = duration
#
#    def render(self):
#        # Render hit of "key" for "duration" amount of seconds
#        # XXX: Currently only uses a string pluck
#        key = (str(self.note), self.duration)
#        if key not in Hit.cache:
#            Hit.cache[key] = source.pluck(self.note, self.duration)
#        return Hit.cache[key]

import numpy as np

def ambient_note(freq, length, decay=0.998, rate=44100):
    """
    Create an ambient, mellow note at the given frequency using a sine wave
    with a smooth attack and release envelope.
    """
    freq = float(freq)
    t = np.linspace(0, length, int(length * rate), endpoint=False)
    
    # Generate a sine wave at the given frequency
    sine_wave = np.sin(2 * np.pi * freq * t)
    
    # Create a smooth attack and release envelope
    attack_time = 0.1  # Adjust the attack time as desired
    release_time = 0.1  # Adjust the release time as desired
    attack_samples = int(attack_time * rate)
    release_samples = int(release_time * rate)
    sustain_samples = len(sine_wave) - attack_samples - release_samples
    
    envelope = np.concatenate([
        np.linspace(0, 1, attack_samples),
        np.ones(sustain_samples),
        np.linspace(1, 0, release_samples)
    ])
    
    # Apply the envelope to the sine wave
    note = sine_wave * envelope
    
    # Apply a gentle lowpass filter to smooth the note
    b = [0.2, 0.2, 0.2, 0.2, 0.2]
    a = [1.0]
    note = np.convolve(note, b, mode='same')
    
    return note

class Hit:
    '''
    Rough draft of Hit class. Stores information about the hit and generates
    the audio array accordingly. Currently implements a basic cache to avoid
    having to rerender identical hits
    '''
    cache = {}

    def __init__(self, note, duration):
        self.note = note
        self.duration = duration

    def render(self):
        # Render hit of "key" for "duration" amount of seconds
        # XXX: Currently uses the ambient_note function
        key = (str(self.note), self.duration)
        if key not in Hit.cache:
            Hit.cache[key] = ambient_note(self.note.frequency(), self.duration)
        return Hit.cache[key]

class Timeline:

  ''' Rough draft of Timeline class. Handles the timing and mixing of Hits
  '''

  def __init__(self, rate=44100):
    self.rate = rate
    self.hits = defaultdict(list)

  def add(self, time, hit):
    # Add "hit" at "time" seconds in
    self.hits[time].append(hit)

  def calculate_length(self):
    # Determine length of playback from end of last hit
    length = 0.0
    for time, hits in self.hits.items():
      for hit in hits:
        length = max(length, time + hit.length)
    return length

  def render(self):
    # Return timeline as audio array by rendering the hits
    total_duration = max(time + hit.duration for time, hits in self.hits.items() for hit in hits)
    length = int(total_duration * self.rate)
    out = np.zeros(length)

    for time, hits in self.hits.items():
        index = int(time * self.rate)
        for hit in hits:
            data = hit.render()

            # Ensure that the data array fits within the remaining space in out
            remaining_space = len(out) - index
            if len(data) > remaining_space:
                data = data[:remaining_space]
            elif len(data) < remaining_space:
                data = np.pad(data, (0, remaining_space - len(data)), 'constant')

            out[index:index + len(data)] += data

    return out