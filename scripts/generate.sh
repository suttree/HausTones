#!/bin/bash

# Remove all .wav files from the output directory
rm /home/pi/src/pele/output/*.wav

# List of melody scripts
melodies=(
    "melodies/wed.py"
    "melodies/thu.py"
    "melodies/swi.py"
    "melodies/genevive.py"
    "melodies/fea.py"
    "melodies/beats.py"
    "melodies/mor.py"
    "melodies/fie.py"
    "melodies/jun.py"
    "melodies/fas.py"
    "melodies/bey.py"
    "melodies/cop.py"
    "melodies/sun.py"
    "melodies/bea.py"
    "melodies/jul.py"
    "melodies/cia.py"
    "melodies/hoo.py"
    "melodies/hto.py"
    "melodies/wai.py"
    "melodies/oud.py"
    "melodies/tie.py"
    "melodies/cle.py"
    "melodies/bee.py"
    "melodies/tre.py"
    "melodies/bel.py"
    "melodies/bel2.py"
    "melodies/deets.py"
    "melodies/ren.py"
    "melodies/exh.py"
    "melodies/zof.py"
)

# Get the total number of melodies
total_melodies=${#melodies[@]}

# Generate a random number of melodies to execute
num_melodies_to_run=$((RANDOM % total_melodies + 1))

# Shuffle the melodies array and pick the first $num_melodies_to_run elements
shuffled_melodies=($(shuf -e "${melodies[@]}" | head -n $num_melodies_to_run))

# Execute the selected melodies
for melody in "${shuffled_melodies[@]}"; do
    python3 "$melody"
done
