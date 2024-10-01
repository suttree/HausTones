import os
import random
import time
from pydub import AudioSegment

demo_folder = "demo"

def generate_silence(duration_ms):
    return AudioSegment.silent(duration=duration_ms)

def play_demo_files():
    wav_files = [file for file in os.listdir(demo_folder) if file.endswith(".wav")]

    for file in wav_files:
        os.system("amixer sset 'Master' 25%")
        
        audio = AudioSegment.from_wav(os.path.join(demo_folder, file))

        low_pass_audio = audio.low_pass_filter(200)

        temp_file = "temp.wav"
        low_pass_audio.export(temp_file, format="wav")

        print(f"Playing: {file}")
        os.system(f"aplay {temp_file}")

        os.remove(temp_file)

        silent_audio = generate_silence(30000)  # 30 seconds in milliseconds
        silent_audio.export("silent.wav", format="wav")
        os.system("aplay silent.wav")
        os.remove("silent.wav")

        sleep_duration = random.randint(30, 90)
        print(f"Sleeping for {sleep_duration} seconds...")
        time.sleep(sleep_duration)

play_demo_files()