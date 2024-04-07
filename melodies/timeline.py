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
    
    # Adjust attack and release times based on the length of the note
    attack_time = min(length * 0.1, 1.0)  # Limit attack time to 10% of the note length or 1.0 seconds
    release_time = min(length * 0.1, 1.5)  # Limit release time to 10% of the note length or 1.5 seconds
    attack_samples = int(attack_time * rate)
    release_samples = int(release_time * rate)
    sustain_samples = len(sine_wave) - attack_samples - release_samples
    
    if sustain_samples < 0:
        # If sustain_samples is negative, adjust attack and release samples
        attack_samples = int(len(sine_wave) * attack_time / (attack_time + release_time))
        release_samples = len(sine_wave) - attack_samples
        sustain_samples = 0
    
    envelope = np.concatenate([
        np.linspace(0, 1, attack_samples),
        np.ones(sustain_samples),
        np.linspace(1, 0, release_samples)
    ])
    
    # Apply the envelope to the sine wave
    note = sine_wave * envelope
    
    # Apply a gentle lowpass filter to smooth the note
    b = [0.1] * 15  # Increase the filter length for more smoothing
    a = [1.0]
    note = np.convolve(note, b, mode='same')
    
    return note

def bell_tone(freq, length, decay=0.996, rate=44100):
    """
    Create a simple bell tone at the given frequency using a combination of sine waves.
    """
    freq = float(freq)
    t = np.linspace(0, length, int(length * rate), endpoint=False)
    
    # Generate sine waves at different harmonics
    fundamental = np.sin(2 * np.pi * freq * t)
    third_harmonic = np.sin(2 * np.pi * freq * 3 * t) * 0.5
    fifth_harmonic = np.sin(2 * np.pi * freq * 5 * t) * 0.25
    
    # Combine the sine waves
    bell = fundamental + third_harmonic + fifth_harmonic
    
    # Apply an exponential decay envelope
    envelope = np.exp(-np.linspace(0, length, len(bell)) * (1 - decay))
    bell *= envelope
    
    # Normalize the amplitude
    bell /= np.max(np.abs(bell))
    
    return bell
    
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
            #if len(Hit.cache) % 2 == 0:
            #  Hit.cache[key] = source.pluck(self.note.frequency(), self.duration) # original
            #else:
            #  Hit.cache[key] = source.electronic_pluck(self.note.frequency(), self.duration) # VIBES

            #  Hit.cache[key] = source.pluck(self.note.frequency(), self.duration) # original            
            Hit.cache[key] = source.electronic_pluck(self.note.frequency(), self.duration) # VIBES

            #Hit.cache[key] = source.soft_ambient_pluck(self.note.frequency(), self.duration)
            #Hit.cache[key] = source.sustained_pluck(self.note.frequency(), self.duration)
            #Hit.cache[key] = source.rounded_pluck(self.note.frequency(), self.duration)
            #Hit.cache[key] = source.ambient_pluck(self.note.frequency(), self.duration)
            #Hit.cache[key] = source.pluck2(self.note.frequency(), self.duration)
            #Hit.cache[key] = ambient_note(self.note.frequency(), self.duration)
            #Hit.cache[key] = bell_tone(self.note.frequency(), self.duration)
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
            if len(data) != remaining_space:
                data = data[:remaining_space]
                data = np.pad(data, (0, remaining_space - len(data)), 'constant')
            
            # Add the rendered data to the output array
            out[index:index + len(data)] += data

    return out