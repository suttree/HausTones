from pydub import AudioSegment, playback
import math

# Constants for audio synthesis
SAMPLE_RATE = 44100  # Hz
DURATION = 1000  # Milliseconds for each note

def generate_scale(root_freq, scale_intervals):
    """ Generate a scale based on root frequency and scale intervals """
    return [root_freq * math.pow(2, i/12) for i in scale_intervals]

def synthesize_notes(scale):
    """ Synthesize the notes of the scale """
    notes = []
    for freq in scale:
        samples = [int(math.sin(2 * math.pi * freq * t / SAMPLE_RATE) * 32767)
                   for t in range(0, int(SAMPLE_RATE * DURATION / 1000))]
        sound = AudioSegment(samples=bytes(samples), sample_width=2, frame_rate=SAMPLE_RATE, channels=1)
        notes.append(sound)
    return notes

def play_notes(notes):
    """ Play the notes in a strumming pattern """
    for note in notes:
        playback.play(note)

def main():
    # Define a major scale (W-W-H-W-W-W-H)
    scale_intervals = [0, 2, 4, 5, 7, 9, 11, 12]
    root_freq = 440  # A4

    # Generate and synthesize scale
    scale = generate_scale(root_freq, scale_intervals)
    notes = synthesize_notes(scale)

    # Loop indefinitely
    while True:
        play_notes(notes)

if __name__ == "__main__":
    main()
