import os
import random
import time
import subprocess

# Path to the 'melodies' folder
melodies_folder = 'melodies'

while True:
    # List all files in the 'melodies' folder
    melodies_files = [file for file in os.listdir(melodies_folder) if file.endswith('.py')]

    if not melodies_files:
        print("No Python scripts found in the 'melodies' folder.")
        break

    # Select a random script from the list
    selected_script = random.choice(melodies_files)

    # Run the selected script using subprocess
    script_path = os.path.join(melodies_folder, selected_script)
    print(f"Running script: {script_path}")
    subprocess.run(['python3', script_path])

    # Sleep for a minute
    time.sleep(60)