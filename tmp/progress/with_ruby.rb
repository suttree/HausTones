require 'audio'
require 'audio/sf'
include Audio

# Parameters
duration = 10.0  # Duration of the tone in seconds
frequency = 440.0  # Frequency of the sine wave (440 Hz for A4)

# Generate the sine wave
samples_per_second = 44100  # Sample rate (CD quality)
num_samples = (duration * samples_per_second).to_i
sine_wave = (0...num_samples).map do |i|
  Math.sin(2 * Math::PI * frequency * i / samples_per_second)
end

# Create an AudioStream
audio_stream = AudioStream.new(samples_per_second, 16, 1)

# Add the sine wave to the AudioStream
audio_stream.add(:mono, sine_wave)

# Play the audio
audio_stream.start.play

# Sleep for the duration of the tone
sleep(duration)

# Stop the audio playback
audio_stream.stop

