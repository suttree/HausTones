import math

# Initialize your variable
x = 5.0

# Define parameters for the oscillation
amplitude = 0.5  # Amplitude of the oscillation (controls the range)
frequency = 0.25  # Frequency of the oscillation (controls how fast it changes)

# Time step
time_step = 0.1

for _ in range(40):
    # Calculate the value to add or subtract using sine wave
    modulation = amplitude * math.sin(frequency * _)
    
    # Add the modulation to the variable
    x += modulation
    
    # Ensure x stays within the range [5, 6]
    x = min(max(x, 5), 6)
    
    # Print the updated value
    print(x)
