# HausTones

codenamne pele, the sad ex-bofriend genererator

Wind chimes, haus vibes, pele.

## Install
sudo apt-get install alsa-tools alsa-utils

https://github.com/pimoroni/pirate-audio

sudo raspi-config and ensure audio output is not HDMI/headphones/etc

/boot/config.txt
dtparam=audio=off
dtoverlay=hifiberry-dac
gpio=25=op,dh

## todo

- controller script
	- don't sleep and then run again, wait for the thread to finish
- remove the squelchy script
- try this line of code
	- varb = duration + min(max(duration + (1 - math.cos(time.time())), -1.0), 1.0)

- master script to run the melody chains
- folder of melodies
- create a squelchy melody
- create a random melody
- create a meldoy based on chord progressions

- fade in and out rain/ambient effects
- alter volume during day (loud mode vs quiet mode)
