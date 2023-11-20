import noise
import time

# Initialize your variable
x = 5.0

# Define parameters for the oscillation
amplitude = 0.5  # Amplitude of the oscillation (controls the range)
frequency = 1.0  # Frequency of the Perlin noise (controls how fast it changes)

# Time step
time_step = 0.1

# Set a seed value for the Perlin noise (optional)
seed = int(time.time())

for _ in range(40):
    # Calculate the Perlin noise value
    perlin_value = noise.pnoise1(_, octaves=1, persistence=0.5, lacunarity=2.0, base=seed)
    
    # Map the Perlin noise value to the desired range [5, 6]
    mapped_value = 5.0 + amplitude * (perlin_value + 1.0) / 2.0
    
    # Update the variable
    x = mapped_value
    
    # Ensure x stays within the range [5, 6]
    x = min(max(x, 5), 6)
    
    # Print the updated value
    print(x)
