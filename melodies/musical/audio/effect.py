from . import source

import noise, time
from noise import pnoise2
import numpy as np

# TODO: More effects. Distortion, echo, delay, reverb, phaser, pitch shift?
# TODO: Better generalize chorus/flanger (they share a lot of code)

import numpy as np

def modulated_delay(data, modwave, dry, wet):
    ''' Use LFO "modwave" as a delay modulator (no feedback)
    '''
    out = data.copy()
    for i in range(len(data)):
        index = int(i - modwave[i])
        if index >= 0 and index < len(data):
            out[i] = np.clip(out[i] * dry + data[index] * wet, -1.0, 1.0)
    return out

def feedback_modulated_delay(data, modwave, dry, wet):
    ''' Use LFO "modwave" as a delay modulator (with feedback)
    '''
    out = data.copy()
    for i in range(len(data)):
        index = int(i - modwave[i])
        if index >= 0 and index < len(data):
            out[i] = np.clip(out[i] * dry + out[index] * wet, -1.0, 1.0)
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

def shimmer_wobble(data, scale=0.3147, depth=0.5, freq=5.0, rate=44100):
    length = float(len(data)) / rate
    now = time.time()
    
    # Generate Perlin noise for brightness
    perlin_brightness = pnoise2(now * scale, length * scale, octaves=5, persistence=0.75, lacunarity=2.2)
    
    # Generate Perlin noise for wobbliness
    perlin_wobble = pnoise2((now + 1000) * scale, length * scale, octaves=3, persistence=0.5, lacunarity=1.5)
    
    # Apply brightness modulation
    brightness_mod = (perlin_brightness + 1) / 2  # Normalize to range [0, 1]
    brightness_mod = np.power(brightness_mod, 2)  # Increase the brightness
    data_bright = data * brightness_mod
    
    # Apply wobble modulation
    wobble_mod = (perlin_wobble + 1) / 2  # Normalize to range [0, 1]
    wobble_mod = wobble_mod * 2 - 1  # Scale to range [-1, 1]
    wobble_mod = np.sin(wobble_mod * freq * np.pi * 2)  # Apply sinusoidal wobble
    data_wobble = data_bright + (data_bright * wobble_mod * depth)
    
    return data_wobble

def reverb(data, delay=50, decay=0.5, wet=0.5, rate=44100):
    ''' Reverb effect
    '''
    out = data.copy()
    delay_samples = int(delay * rate / 1000)
    decay_samples = int(decay * rate)
    
    for i in range(delay_samples, len(data)):
        out[i] += out[i - delay_samples] * decay
    
    return (data * (1 - wet)) + (out * wet)

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