# Parameters
duration = 10.0  # Duration of the tone in seconds
frequency = 440.0  # Frequency of the sine wave (440 Hz for A4)
sample_rate = 44100  # Sample rate (CD quality)

# Calculate the number of samples
num_samples = (duration * sample_rate).to_i

# Create an array to store the audio samples
samples = (0...num_samples).map do |i|
  Math.sin(2 * Math::PI * frequency * i / sample_rate)
end

# Open a WAV file for writing
File.open('ambient_tone.wav', 'wb') do |file|
  # WAV header
  file.write("RIFF")
  file.write([36 + num_samples * 2].pack("V"))
  file.write("WAVE")
  file.write("fmt ")
  file.write([16].pack("V"))
  file.write([1].pack("v"))
  file.write([1].pack("v"))
  file.write([sample_rate].pack("V"))
  file.write([sample_rate * 2].pack("V"))
  file.write([2].pack("v"))
  file.write([16].pack("v"))
  file.write("data")
  file.write([num_samples * 2].pack("V"))
  
  # Write audio samples as 16-bit signed integers
  samples.each do |sample|
    file.write([(sample * 32767).to_i].pack("s"))
  end
end

# Play the generated WAV file using a system audio player (e.g., `aplay` on Linux)
system('aplay ambient_tone.wav')

# You can use different system audio players for different platforms (e.g., `afplay` on macOS, `play` on Windows)
