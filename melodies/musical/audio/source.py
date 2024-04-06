import math
import numpy

def silence(length, rate=44100):
    ''' Generate 'length' seconds of silence at 'rate'
    '''
    return numpy.zeros(int(length * rate))


def pygamesound(sound):
    ''' Create numpy array from pygame sound object
        rate is determined by pygame.mixer settings
    '''
    import pygame
    pygame.sndarray.use_arraytype('numpy')
    array = pygame.sndarray.array(sound)
    rate, format, channels = pygame.mixer.get_init()
    data = numpy.zeros(len(array))
    for i, sample in enumerate(array):
        data[i] = sum(sample)
    if format < 0:
        data /= (2 ** -format) / 2
    else:
        data = (data / (2 ** format)) * 2 - 1
    return data


def generate_wave_input(freq, length, rate=44100, phase=0.0):
    ''' Used by waveform generators to create frequency-scaled input array

        Courtesy of threepineapples:
          https://code.google.com/p/python-musical/issues/detail?id=2
    '''
    length = int(length * rate)
    t = numpy.arange(length) / float(rate)
    omega = float(freq) * 2 * math.pi
    phase *= 2 * math.pi  
    return omega * t + phase


def sine(freq, length, rate=44100, phase=0.0):
    ''' Generate sine wave for frequency of 'length' seconds long
        at a rate of 'rate'. The 'phase' of the wave is the percent (0.0 to 1.0)
        into the wave that it starts on.
    '''
    data = generate_wave_input(freq, length, rate, phase)
    return numpy.sin(data)


def _sawtooth(t):
    ''' Generate sawtooth wave from wave input array.
    '''
    tmod = numpy.mod(t, 2 * numpy.pi)
    return (tmod / numpy.pi) - 1


def sawtooth(freq, length, rate=44100, phase=0.0):
    ''' Generate sawtooth wave for frequency of 'length' seconds long
        at a rate of 'rate'. The 'phase' of the wave is the percent (0.0 to 1.0)
        into the wave that it starts on.
    '''
    data = generate_wave_input(freq, length, rate, phase)
    return _sawtooth(data)


def _square(t, duty=0.5):
    ''' Generate square wave from wave input array with specific 'duty'.
    '''
    y = numpy.zeros(t.shape)
    tmod = numpy.mod(t, 2 * numpy.pi)
    mask = tmod < duty * 2 * numpy.pi
    numpy.place(y, mask, 1)
    numpy.place(y, (1 - mask), -1)
    return y


def square(freq, length, rate=44100, phase=0.0):
    ''' Generate square wave for frequency of 'length' seconds long
        at a rate of 'rate'. The 'phase' of the wave is the percent (0.0 to 1.0)
        into the wave that it starts on.
    '''
    data = generate_wave_input(freq, length, rate, phase)
    return _square(data)

ringbuffer_cache = {}
def ringbuffer(data, length, decay=1.0, rate=44100):
    ''' Repeat data for 'length' amount of time, smoothing to reduce higher
        frequency oscillation. decay is the percent of amplitude decrease.
    '''
    key = (hash(f"{data}-{length}-{decay}-{rate}"))
    if key not in ringbuffer_cache:
        phase = len(data)
        length = int(rate * length)
        out = numpy.resize(data, length)
        for i in range(phase, length):
            index = i - phase
            out[i] = (out[index] + out[index + 1]) * 0.5 * decay
            ringbuffer_cache[key] = out
    #return out
    return ringbuffer_cache[key]


def pluck(freq, length, decay=0.998, rate=44100):
    ''' Create a pluck noise at freq by sending white noise through a ring buffer
        http://en.wikipedia.org/wiki/Karplus-Strong_algorithm
    '''
    freq = float(freq)
    phase = int(rate / freq)
    data = numpy.random.random(phase) * 2 - 1
    return ringbuffer(data, length, decay, rate)

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