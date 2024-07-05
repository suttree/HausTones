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

import numpy as np

import numpy as np

def piano_pluck(freq, length, decay=0.996, rate=44100, brightness=0.5):
    """
    Create a piano-like pluck sound at the given frequency.
    
    :param freq: Frequency of the note
    :param length: Length of the sound in seconds
    :param decay: Decay factor (0.996 gives a more piano-like sustain)
    :param rate: Sample rate
    :param brightness: Controls the brightness of the tone (0 to 1)
    """
    freq = float(freq)
    phase = int(rate / freq)
    
    # Generate initial excitation using a combination of sine waves
    harmonics = [1, 2, 3, 4, 5]
    excitation = np.zeros(phase)
    for harmonic in harmonics:
        amplitude = 1 / harmonic
        excitation += amplitude * np.sin(np.linspace(0, harmonic * np.pi * 2, phase))
    
    # Normalize the excitation
    excitation /= np.max(np.abs(excitation))
    
    # Apply brightness control
    excitation = excitation * brightness + (1 - brightness) * np.random.rand(phase)
    
    # Create the output buffer
    num_samples = int(length * rate)
    output = np.zeros(num_samples)
    
    # Karplus-Strong algorithm with modifications for piano-like sound
    for i in range(num_samples):
        output[i] = excitation[i % phase]
        excitation[i % phase] = decay * 0.5 * (excitation[i % phase] + excitation[(i + 1) % phase])
        
        # Add a slight pitch modulation for more natural sound
        if i % 1000 == 0:
            phase = int(rate / (freq + np.random.uniform(-0.1, 0.1)))
    
    return output

# Example usage
# You'll need to implement or import a function to play the audio
# play_audio(piano_pluck(440, 2, brightness=0.7))

def dulcimer_pluck(freq, length, decay=0.9985, rate=44100, brightness=0.8):
    """
    Create a dulcimer-like pluck sound at the given frequency.
    
    :param freq: Frequency of the note
    :param length: Length of the sound in seconds
    :param decay: Decay factor (0.9985 gives a quicker decay typical of dulcimers)
    :param rate: Sample rate
    :param brightness: Controls the brightness of the tone (0 to 1)
    """
    freq = float(freq)
    initial_phase = int(rate / freq)
    
    # Generate initial excitation using a combination of sine waves
    # Dulcimers have strong odd harmonics
    harmonics = [1, 3, 5, 7, 9]
    excitation = np.zeros(initial_phase)
    for i, harmonic in enumerate(harmonics):
        amplitude = 1 / (i + 1)**1.5  # Faster decay of higher harmonics
        excitation += amplitude * np.sin(np.linspace(0, harmonic * np.pi * 2, initial_phase))
    
    # Add some noise to simulate the hammer strike
    excitation += np.random.rand(initial_phase) * 0.1
    
    # Normalize the excitation
    excitation /= np.max(np.abs(excitation))
    
    # Apply brightness control
    excitation = excitation * brightness + (1 - brightness) * np.random.rand(initial_phase)
    
    # Create the output buffer
    num_samples = int(length * rate)
    output = np.zeros(num_samples)
    
    # Modified Karplus-Strong algorithm for dulcimer-like sound
    phase = initial_phase
    for i in range(num_samples):
        output[i] = excitation[i % initial_phase]
        # Dulcimer strings have a brighter attack and quicker decay
        if i < rate * 0.01:  # First 10ms
            decay_factor = decay * 0.999
        else:
            decay_factor = decay
        excitation[i % initial_phase] = decay_factor * 0.5 * (excitation[i % initial_phase] + excitation[(i - 1) % initial_phase])
        
        # Add a slight pitch modulation for more natural sound
        if i % 500 == 0:  # More frequent modulation for dulcimer's tighter strings
            phase = int(rate / (freq + np.random.uniform(-0.2, 0.2)))
            phase = max(min(phase, initial_phase * 2), initial_phase // 2)  # Limit phase variation
    
    return output

# Example usage
# You'll need to implement or import a function to play the audio
# play_audio(dulcimer_pluck(440, 2, brightness=0.8))

def violin_note(freq, length, vibrato_rate=5, vibrato_depth=0.3, volume_envelope=None, rate=44100):
    """
    Create a violin-like sustained note at the given frequency.
    
    :param freq: Fundamental frequency of the note
    :param length: Length of the sound in seconds
    :param vibrato_rate: Rate of vibrato in Hz
    :param vibrato_depth: Depth of vibrato (percentage of fundamental frequency)
    :param volume_envelope: Optional array defining the volume envelope
    :param rate: Sample rate
    """
    # Generate time array
    t = np.linspace(0, length, int(length * rate), endpoint=False)
    
    # Generate vibrato
    vibrato = vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)
    
    # Generate the fundamental and harmonics
    num_harmonics = 15
    signal = np.zeros_like(t)
    for n in range(1, num_harmonics + 1):
        # Violin harmonics typically decrease in amplitude as 1/n^2
        harmonic_amp = 1.0 / (n ** 2)
        
        # Even harmonics are typically weaker in bowed string instruments
        if n % 2 == 0:
            harmonic_amp *= 0.5
        
        harmonic_freq = n * freq
        signal += harmonic_amp * np.sin(2 * np.pi * harmonic_freq * (t + vibrato/harmonic_freq))
    
    # Normalize the signal
    signal /= np.max(np.abs(signal))
    
    # Apply volume envelope
    if volume_envelope is None:
        # Default envelope: quick attack, long sustain, gentle release
        attack = int(rate * 0.1)  # 100ms attack
        release = int(rate * 0.3)  # 300ms release
        sustain_level = 0.8
        
        envelope = np.ones_like(signal) * sustain_level
        envelope[:attack] = np.linspace(0, sustain_level, attack)
        envelope[-release:] = np.linspace(sustain_level, 0, release)
    else:
        envelope = np.interp(np.linspace(0, 1, len(signal)), np.linspace(0, 1, len(volume_envelope)), volume_envelope)
    
    signal *= envelope
    
    # Add some noise to simulate bow noise
    bow_noise = np.random.normal(0, 0.005, len(signal))
    signal += bow_noise
    
    # Final normalization
    signal /= np.max(np.abs(signal))
    
    return signal

# Example usage
# You'll need to implement or import a function to play the audio
# play_audio(violin_note(440, 3, vibrato_rate=6, vibrato_depth=0.3))

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

def bell_tone(freq, length, attack=0.01, decay=0.2, sustain_level=0.6, release=0.5, rate=44100):
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
    
    # Apply ADSR envelope
    envelope = adsr_envelope(len(bell), attack, decay, sustain_level, release, rate)
    bell *= envelope
    
    # Normalize the amplitude
    bell /= np.max(np.abs(bell))
    
    return bell

def adsr_envelope(length, attack, decay, sustain_level, release, rate=44100):
    attack_samples = int(attack * rate)
    decay_samples = int(decay * rate)
    release_samples = int(release * rate)
    sustain_samples = length - attack_samples - decay_samples - release_samples

    envelope = np.zeros(length)
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    envelope[attack_samples:attack_samples+decay_samples] = np.linspace(1, sustain_level, decay_samples)
    envelope[attack_samples+decay_samples:attack_samples+decay_samples+sustain_samples] = sustain_level
    envelope[-release_samples:] = np.linspace(sustain_level, 0, release_samples)

    return envelope

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

    def render(self, style):
        # Render hit of "key" for "duration" amount of seconds
        key = (str(self.note), self.duration, style)
        if key not in Hit.cache:
            #  Hit.cache[key] = source.pluck(self.note.frequency(), self.duration) # original

            frequency = self.note.frequency()
            # Apply a small random frequency variation
            frequency *= 1 + np.random.normal(0, 0.01)
            
            if style == 1:
              Hit.cache[key] = source.electronic_pluck(frequency, self.duration) # VIBES              
                #source.electronic_pluck
              #source.soft_pluck
                #source.soft_ambient_pluck
              #source.sustained_pluck
              #source.ambient_pluck
              #source.solfeggio_pluck
                #source.sine
            elif style == 2:
              Hit.cache[key] = ambient_note(frequency, self.duration) # WHALES
            elif style == 3:
              Hit.cache[key] = bell_tone(frequency, self.duration) # VURBZ
            elif style == 4:
              Hit.cache[key] = piano_pluck(frequency, self.duration)
            elif style == 5:
              Hit.cache[key] = dulcimer_pluck(frequency, self.duration)
            elif style == 6:
              Hit.cache[key] = violin_note(frequency, self.duration)

            
            #if self.duration % 2 < 0.5:
            #   Hit.cache[key] = bell_tone(self.note.frequency(), self.duration)
            #elif self.duration % 2 < 1.0:
            #  Hit.cache[key] = source.electronic_pluck(self.note.frequency(), self.duration) # VIBES
            #else:
            #    Hit.cache[key] = ambient_note(self.note.frequency(), self.duration)
            
            #Hit.cache[key] = ambient_note(self.note.frequency(), self.duration)
            #Hit.cache[key] = bell_tone(self.note.frequency(), self.duration)
            #Hit.cache[key] = source.electronic_pluck(self.note.frequency(), self.duration) # VIBES

            #Hit.cache[key] = source.solfeggio_pluck(self.note.frequency(), self.duration) # VIBES?!??!
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

  def render(self, style = 1):
    # Return timeline as audio array by rendering the hits
    total_duration = max(time + hit.duration for time, hits in self.hits.items() for hit in hits)
    length = int(total_duration * self.rate)
    out = np.zeros(length)

    for time, hits in self.hits.items():
        index = int(time * self.rate)
        for hit in hits:
            data = hit.render(style)

            # Ensure that the data array fits within the remaining space in out
            remaining_space = len(out) - index
            if len(data) != remaining_space:
                data = data[:remaining_space]
                data = np.pad(data, (0, remaining_space - len(data)), 'constant')
            
            # Add the rendered data to the output array
            out[index:index + len(data)] += data

    out = np.interp(out, (out.min(), out.max()), (-1, 1))

    return out