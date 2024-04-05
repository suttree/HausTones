from collections import defaultdict
from musical.audio import source
import numpy as np

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

    def render(self, sample_rate):
        # Render hit of "key" for "duration" amount of seconds
        # XXX: Currently only uses a string pluck
        key = (str(self.note), self.duration)
        if key not in Hit.cache:
            Hit.cache[key] = source.pluck(self.note, self.duration, sample_rate)
        return Hit.cache[key]

class Timeline:
    '''
    Rough draft of Timeline class. Handles the timing and mixing of Hits
    '''
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.hits = defaultdict(list)

    def add(self, time, hit):
        # Add "hit" at "time" seconds in
        self.hits[time].append(hit)

    def calculate_length(self):
        # Determine length of playback from end of last hit
        end_time = 0.0
        for time, hits in self.hits.items():
            for hit in hits:
                end_time = max(end_time, time + hit.duration)
        return end_time

    def render(self):
        # Return timeline as audio array by rendering the hits
        num_samples = int(self.calculate_length() * self.sample_rate)
        out = np.zeros(num_samples)

        for time, hits in self.hits.items():
            index = int(time * self.sample_rate)
            for hit in hits:
                data = hit.render(self.sample_rate)
                out[index:index + len(data)] += data[:len(out) - index]

        return out