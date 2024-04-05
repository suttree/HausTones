import numpy as np
import wave
import struct
import os
import tempfile

# Solfeggio frequencies
FREQUENCIES = {
    'UT': 396,
    'RE': 417,
    'MI': 528,
    'FA': 639,
    'SOL': 741,
    'LA': 852,
    'SI': 963
}

def generate_tone(frequency, duration, volume=0.1, sample_rate=44100):
    time_points = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    tone = volume * np.sin(2 * np.pi * frequency * time_points)
    return tone.astype(np.float32)

def save_tone_to_wav(tone, sample_rate, filename):
    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, 0, 'NONE', 'not compressed'))
        for sample in tone:
            wav_file.writeframes(struct.pack('h', int(sample * 32767)))

def play_tone(tone, sample_rate):
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        save_tone_to_wav(tone, sample_rate, temp_file.name)
        os.system(f"afplay {temp_file.name}")
        os.unlink(temp_file.name)

def lerp(start, end, t):
    return start + (end - start) * t

def main():
    print("Playing Solfeggio tones with continuous lerping:")
    tone_duration = 4
    lerp_duration = 1
    sample_rate = 44100
    
    tones = list(FREQUENCIES.values())
    num_tones = len(tones)
    
    for i in range(num_tones):
        curr_freq = tones[i]
        next_freq = tones[(i + 1) % num_tones]
        
        print(f"Playing tone at {curr_freq} Hz")
        main_tone = generate_tone(curr_freq, tone_duration, volume=0.1, sample_rate=sample_rate)
        
        print(f"Lerping from {curr_freq} Hz to {next_freq} Hz")
        lerp_tone = np.zeros(int((tone_duration + lerp_duration) * sample_rate), dtype=np.float32)
        
        # Generate the main tone
        lerp_tone[:int(tone_duration * sample_rate)] = main_tone
        
        # Generate the lerping tone
        for j in range(int(tone_duration * sample_rate), len(lerp_tone)):
            t = (j - int(tone_duration * sample_rate)) / (int(lerp_duration * sample_rate) - 1)
            lerp_freq = lerp(curr_freq, next_freq, t)
            lerp_tone[j] = generate_tone(lerp_freq, 1 / sample_rate, volume=0.1)[0]
        
        play_tone(lerp_tone, sample_rate)

if __name__ == '__main__':
    main()
