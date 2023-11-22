import os
import random
import time
import subprocess
import threading

# Path to the 'melodies' folder
melodies_folder = 'melodies'

def run_melody(script_path):
    try:
        subprocess.run(['python3', script_path], check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to run the script: {script_path}")

while True:
    # List all files in the 'melodies' folder
    melodies_files = [file for file in os.listdir(melodies_folder) if file.endswith('.py')]

    if not melodies_files:
        print("No Python scripts found in the 'melodies' folder.")
        break

    # Select a random script from the list
    selected_script = random.choice(melodies_files)

    # Run the selected script in a separate thread
    script_path = os.path.join(melodies_folder, selected_script)
    print(f"Running script: {script_path}")

    melody_thread = threading.Thread(target=run_melody, args=(script_path,))
    melody_thread.start()

    # Wait for the thread to complete before moving to the next file
    melody_thread.join()

    # Optionally, you can still have a small sleep here, but it's not necessary for the threading logic
    time.sleep(60)