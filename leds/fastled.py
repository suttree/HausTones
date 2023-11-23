# The FastLED "100-lines-of-code" demo reel, adapted to work with the BlinkStick
# line of products.
#
# Originally by: Mark Kriegsman (https://github.com/FastLED/FastLED/blob/master/examples/DemoReel100/DemoReel100.ino)
# Ported to Python and Blinkstick by Different55

from blinkstick import blinkstick
from time import time, sleep
from colorsys import hsv_to_rgb
from random import randint,random
from math import sin, pi

stick = None
count = 0

for i in blinkstick.find_all(): # Loop through all connected BlinkSticks
	if i.get_led_count() > 0: # Find the first one with multiple LEDs
		stick = i
		count = i.get_led_count()
		break

# ------------------------

def map_data(minimum, maximum):
	mapped_data = data[:]
	for i in range(len(data)):
		val = data[i]
		mapped_data[i] = int(map(val, minimum, maximum))
	return mapped_data

def map(val, min, max):
	difference = max-min
	new_val = (val*difference+min)
	return new_val

def set_led(index, new):
	data[index*3:index*3+3] = new

def add_led(index, new):
	old = data[index*3:index*3+3]
	data[index*3:index*3+3] = [min(1, o+n) for o,n in zip(old, new)]

def rainbow():
	new = []
	for i in range(count):
		(r, g, b) = hsv_to_rgb(i/(count-1), 1, 1)
		new.extend([g, r, b])
	fade_to(new, 0.15)

def rainbow_glitter():
	rainbow()
	add_glitter(80)

def add_glitter(chance):
	if (randint(0, 255) < chance):
		set_led(randint(0, count-1), [1, 1, 1])

def fade_by(amount):
	for i in range(len(data)):
		data[i] *= 1-amount

def fade_to(new, amount):
	for i in range(len(data)):
		oldval = data[i]
		newval = new[i]
		data[i] = (1-amount)*oldval + amount*newval

def confetti():
	fade_by(.04)
	pos = randint(0, count-1)
	(r, g, b) = hsv_to_rgb(current_hue+random()*.25, .75, 1)
	#set_led(pos, [g, r, b])
	add_led(pos, [g, r, b])

def beatsin(bpm, min=0, max=1):
	x = ((time()*2*pi)/60)*bpm
	val = map(sin(x)/2+.5, min, max)
	return val

def sinelon():
	fade_by(.075)
	pos = int(beatsin(13, 0, count-1))
	(r, g, b) = hsv_to_rgb(current_hue, 1, 0.75)
	set_led(pos, [g, r, b])

party_colors = [
	[0x55/0xff, 0x00/0xff, 0xAB/0xff], [0x84/0xff, 0x00/0xff, 0x7C/0xff], [0xB5/0xff, 0x00/0xff, 0x4B/0xff], [0xE5/0xff, 0x00/0xff, 0x1B/0xff],
	[0xE8/0xff, 0x17/0xff, 0x00/0xff], [0xB8/0xff, 0x47/0xff, 0x00/0xff], [0xAB/0xff, 0x77/0xff, 0x00/0xff], [0xAB/0xff, 0xAB/0xff, 0x00/0xff],
	[0xAB/0xff, 0x55/0xff, 0x00/0xff], [0xDD/0xff, 0x22/0xff, 0x00/0xff], [0xF2/0xff, 0x00/0xff, 0x0E/0xff], [0xC2/0xff, 0x00/0xff, 0x3E/0xff],
	[0x8F/0xff, 0x00/0xff, 0x71/0xff], [0x5F/0xff, 0x00/0xff, 0xA1/0xff], [0x2F/0xff, 0x00/0xff, 0xD0/0xff], [0x00/0xff, 0x07/0xff, 0xF9/0xff]
]

def interpolate(a, b, fac):
	return (a + fac * (b - a))

def color_from_palette(pal, pos, brightness):
	pos = pos%1
	brightness = brightness%1
	index = int(pos*len(pal))
	index2 = (index+1)%len(pal)
	factor = (pos*len(pal))%1

	a = pal[index]
	b = pal[(index+1)%len(pal)]

	color = [interpolate(a, b, factor)*brightness for a,b in zip(a,b)]
	return color

def bpm():
	bpm = 62
	beat = beatsin(bpm, .25)
	for i in range(count):
		(r, g, b) = color_from_palette(party_colors, current_hue/256+(i/128), beat-(current_hue/255)+(i*10/255))
		set_led(i, [g, r, b])

def juggle():
	fade_by(0.075)
	for i in range(8):
		pos = int(beatsin(i+7, 0, count-1))
		(r, g, b) = hsv_to_rgb(i/8, 0.8, 1)
		set_led(pos, [g, r, b])

# ------------------------

if stick == None:
	print("Unable to find appropriate blinkstick.")
	exit()

# List of patterns to cycle through. Each is defined as a separate function below.
patterns = [rainbow, rainbow_glitter, confetti, sinelon, bpm, juggle]
data = [0] * count * 3

def loop():
	global current_hue, current_pattern
	current_pattern = int(time()/10) % len(patterns) # Index number of current pattern
	current_hue = (time()*1000)//10/256 # Rotating "base color" used by many patterns
	patterns[current_pattern]()
	remapped = map_data(0, 255)
	stick.set_led_data(0, remapped)

while True:
	loop()
	sleep(0.02)
