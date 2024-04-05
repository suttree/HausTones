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

def play_tone(frequency, duration, volume=0.1, sample_rate=44100):
    tone = generate_tone(frequency, duration, volume, sample_rate)
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        save_tone_to_wav(tone, sample_rate, temp_file.name)
        os.system(f"afplay {temp_file.name}")
        os.unlink(temp_file.name)

def main():
    print("Playing Solfeggio tones:")
    for note, frequency in FREQUENCIES.items():
        print(f"Playing {note} ({frequency} Hz)")
        play_tone(frequency, duration=2)

if __name__ == '__main__':
    main()
