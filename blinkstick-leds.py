import time
import math
import colorsys
from random import randint

from blinkstick import blinkstick

class Main(blinkstick.BlinkStickPro):
    def run(self):
        self.send_data_all()

        red = randint(0, 255)
        green = randint(0, 255)
        blue = randint(0, 255)

        x = 0
        reps = 0
        sign = 1
        try:
            while True:
                self.bstick.set_color(0, x, red, green, blue)
                time.sleep(0.2)

                if reps % 2 == 0:
                    self.bstick.set_color(0, x, 0, 0, 0)
                    time.sleep(0.004)

                x += sign
                if x == self.r_led_count - 1:
                    sign = -1
                    reps += 1
                    red = randint(0, 255)
                    green = randint(0, 255)
                    blue = randint(0, 255)
                elif x == 0:
                    sign = 1
        except KeyboardInterrupt:
            self.off()
            return

# Change the number of LEDs for r_led_count
main = Main(r_led_count=32, max_rgb_value=128)
if main.connect():
    main.run()
else:
    print("No BlinkSticks found")
