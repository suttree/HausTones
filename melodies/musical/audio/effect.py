from . import source

import noise, time
from noise import pnoise2
import numpy as np

# TODO: More effects. Distortion, echo, delay, reverb, phaser, pitch shift?
# TODO: Better generalize chorus/flanger (they share a lot of code)

def modulated_delay(data, modwave, dry, wet):
    ''' Use LFO "modwave" as a delay modulator (no feedback)
    '''
    out = data.copy()
    for i in range(len(data)):
        index = int(i - modwave[i])
        if index >= 0 and index < len(data):
            out[i] = data[i] * dry + data[index] * wet
    return out


def feedback_modulated_delay(data, modwave, dry, wet):
    ''' Use LFO "modwave" as a delay modulator (with feedback)
    '''
    out = data.copy()
    for i in range(len(data)):
        index = int(i - modwave[i])
        if index >= 0 and index < len(data):
            out[i] = out[i] * dry + out[index] * wet
    return out


def chorus(data, freq, dry=0.5, wet=0.5, depth=1.0, delay=25.0, rate=44100):
    ''' Chorus effect
        http://en.wikipedia.org/wiki/Chorus_effect
    '''
    length = float(len(data)) / rate
    mil = float(rate) / 1000
    delay *= mil
    depth *= mil
    modwave = (source.sine(freq, length) / 2 + 0.5) * depth + delay
    return modulated_delay(data, modwave, dry, wet)


def flanger(data, freq, dry=0.5, wet=0.5, depth=20.0, delay=1.0, rate=44100):
    ''' Flanger effect
        http://en.wikipedia.org/wiki/Flanging
    '''
    length = float(len(data)) / rate
    mil = float(rate) / 1000
    delay *= mil
    depth *= mil
    modwave = (source.sine(freq, length) / 2 + 0.5) * depth + delay
    return feedback_modulated_delay(data, modwave, dry, wet)


def tremolo(data, freq, dry=0.5, wet=0.5, rate=44100):
    ''' Tremolo effect
        http://en.wikipedia.org/wiki/Tremolo
    '''
    length = float(len(data)) / rate
    modwave = (source.sine(freq, length) / 2 + 0.5)
    return (data * dry) + ((data * modwave) * wet)


def shimmer(data, scale=0.3147, rate=44100):
    length = float(len(data)) / rate
    now = time.time()
    perlin = pnoise2(now * scale, length * scale, octaves=5, persistence=0.75, lacunarity=2.2)
    return (data * perlin)
    
def pan(data, length, rate=44100, pan_freq=0.5):
    '''
    Apply a slow panning effect from left to right to the audio data.
    '''
    # Generate a sine wave for panning
    t = np.arange(len(data)) / rate
    pan_wave = np.sin(2 * np.pi * pan_freq * t)
    
    # Normalize the panning wave between 0 and 1
    pan_wave = (pan_wave + 1) / 2
    
    # Create left and right channel multipliers
    left_mult = 1 - pan_wave
    right_mult = pan_wave
    
    # Apply panning to the audio data
    left_channel = data * left_mult.reshape(-1, 1)
    right_channel = data * right_mult.reshape(-1, 1)
    
    # Combine the left and right channels
    panned_data = np.hstack((left_channel, right_channel))
    
    return panned_data
    
def panned_tremolo(data, freq, dry=0.5, wet=0.5, rate=44100, pan_freq=0.5):
    '''
    Apply a tremolo effect with slow panning from left to right to the audio data.
    '''
    tremolo_data = tremolo(data, freq, dry, wet, rate)
    panned_data = pan(tremolo_data, len(data) / rate, rate, pan_freq)
    return panned_data