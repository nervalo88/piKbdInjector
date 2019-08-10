import board
import neopixel
import time
import random
import RPi.GPIO as GPIO

pixels = neopixel.NeoPixel(board.D18, 1,brightness=0.1)
pixels[0] = (255, 0, 0)

maxBright = 20
print(GPIO.getmode())
print(GPIO.BCM)
while True:
    for i in range(maxBright):
        pixels.brightness = i/100
        # print(i/100)
        time.sleep(0.1)
        
    for i in range(maxBright):
        pixels.brightness = (maxBright-i)/100
        # print((maxBright-i)/100)
        time.sleep(0.1)
    pixels[0] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    # print (pixels[0])