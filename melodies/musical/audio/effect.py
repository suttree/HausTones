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

def pan(data, pan_amount=0.5):
    ''' Panning effect
    '''
    # Validate pan_amount to be in range [-1, 1]
    pan_amount = max(-1, min(pan_amount, 1))

    # Calculate left and right channel gains based on pan_amount
    left_gain = np.sqrt(0.5 - pan_amount / 2)
    right_gain = np.sqrt(0.5 + pan_amount / 2)

    # Apply panning
    left_channel = data * left_gain
    right_channel = data * right_gain

    # Stack left and right channels horizontally
    panned_audio = np.column_stack((left_channel, right_channel))

    return panned_audio
    
def simple_pan(data, pan_amount=0.5):
    ''' Simple Panning effect
    '''
    # Validate pan_amount to be in range [0, 1]
    pan_amount = max(0, min(pan_amount, 1))

    # Split the audio into left and right channels
    left_channel = data * (1 - pan_amount)
    right_channel = data * pan_amount

    # Stack left and right channels horizontally
    panned_audio = np.column_stack((left_channel, right_channel))

    return panned_audio

def simple_delay(data, delay_samples=1000, feedback=0.5, wet=0.5):
    ''' Simple Delay effect
    '''
    # Create an empty array to store delayed audio
    delayed_audio = np.zeros_like(data)

    # Apply delay effect
    for i in range(delay_samples, len(data)):
        delayed_audio[i] = data[i - delay_samples] + feedback * delayed_audio[i - delay_samples]

    # Mix original and delayed audio
    output_audio = (1 - wet) * data + wet * delayed_audio

    return output_audio