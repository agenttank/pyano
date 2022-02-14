#!/usr/bin/env python3
#
import os
import sys
import time
from rpi_ws281x import *
import argparse
import mido

# LED strip configuration:
LED_COUNT      = 184      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



def colorWipe(strip, color, wait_ms=10):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def pianoChangeColorRainbow(strip, j):
  timeout = 3000
  while True:
    print(timeout)
    for msg in inport.iter_pending():
      print(msg)
      if msg.type == "note_on":
        strip.setPixelColor(round((msg.note - 17) * 2.0), wheel((int(round((msg.note - 17)) * 256 / 88 + j) & 255)))
        strip.setPixelColor(round((msg.note - 17) * 2.0) -1, wheel((int(round((msg.note - 17)) * 256 / 88 + j) & 255)))
        strip.setPixelColor(round((msg.note - 17) * 2.0) +1, wheel((int(round((msg.note - 17)) * 256 / 88 + j) & 255)))
        j += 1
        timeout = 3000
      if msg.type == "note_off":
        strip.setPixelColor(round((msg.note - 17) * 2.0), Color(0,0,0))
        strip.setPixelColor(round((msg.note - 17) * 2.0) -1, Color(0,0,0))
        strip.setPixelColor(round((msg.note - 17) * 2.0) +1, Color(0,0,0))
        timeout = 3000
      strip.show()
      if j > 1279:
        j = 0
    timeout -= 1
    if timeout == 0:
      sys.stdout.flush()
      os.execv(sys.argv[0], sys.argv)
    time.sleep(0.01)


def pianoChangeColorRainbowAllSame(strip, j):
  while True:
    for msg in inport.iter_pending():
      if msg.type == "note_on":
        strip.setPixelColor(round((msg.note - 17) * 2.0), wheel(j & 255))
      if msg.type == "note_off":
        strip.setPixelColor(round((msg.note - 17) * 2.0), Color(0,0,0))
      strip.show()
      j += 1
      if j > 1279:
        j = 0
    time.sleep(0.01)

def pianoColorRainbow(strip):
  while True:
    j=0
    for msg in inport.iter_pending():
      if msg.type == "note_on":
        strip.setPixelColor(round((msg.note - 17) * 2.0), wheel((int(round((msg.note - 17)) * 256 / 88 + j) & 255)))
      if msg.type == "note_off":
        strip.setPixelColor(round((msg.note - 17) * 2.0), Color(0,0,0))
      strip.show()
      j += 1
      if j > 1279:
        j = 0
    time.sleep(0.01)

def pianoChangeColorEachNote(strip):
  i=0
  while True:
    colarray = [Color(255, 0, 24), Color(255, 165, 44), Color(255, 255, 65), Color(0, 128, 24), Color(0, 0, 249), Color(134, 0, 125)]
    for msg in inport.iter_pending():
      if msg.type == "note_on":
        print (i)
        strip.setPixelColor(round((msg.note - 17) * 2.0), colarray[i])
        strip.setPixelColor(round((msg.note - 17) * 2.0) + 1, colarray[i]) 
        strip.setPixelColor(round((msg.note - 17) * 2.0) - 1, colarray[i])
        strip.setPixelColor(round((msg.note - 17) * 2.0) + 2, colarray[i]) 
        strip.setPixelColor(round((msg.note - 17) * 2.0) + 2, colarray[i]) 
        i += 1
      if msg.type == "note_off":
        strip.setPixelColor(round((msg.note - 17) * 2.0) + 1, Color(0,0,0))
        strip.setPixelColor(round((msg.note - 17) * 2.0) + 2, Color(0,0,0))
        strip.setPixelColor(round((msg.note - 17) * 2.0), Color(0,0,0))
        strip.setPixelColor(round((msg.note - 17) * 2.0) - 1, Color(0,0,0))
        strip.setPixelColor(round((msg.note - 17) * 2.0) - 2, Color(0,0,0))
      strip.show()
      if i > 5:
        i = 0
    time.sleep(0.01)
  

def pianoSingleColor(strip, color):
  for msg in inport.iter_pending():
    print (msg)
    if(hasattr(msg, 'note')):
      if msg.type == "note_on":
        strip.setPixelColor(round((msg.note - 17) * 2.0), color)
        strip.setPixelColor(round((msg.note - 17) * 2.0) + 1, color) 
        strip.setPixelColor(round((msg.note - 17) * 2.0) - 1, color)
      if msg.type == "note_off":
        strip.setPixelColor(round((msg.note - 17) * 2.0) + 1, Color(0,0,0))
        strip.setPixelColor(round((msg.note - 17) * 2.0), Color(0,0,0))
        strip.setPixelColor(round((msg.note - 17) * 2.0) - 1, Color(0,0,0))
      strip.show()
    time.sleep(0.05)
        
# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
    
    while True:
      try:
        inport=mido.open_input('Clavinova:Clavinova MIDI 1 20:0')
        pianoChangeColorRainbow(strip, 0)
#        pianoSingleColor(strip, Color(10, 30, 230))
#        pianoChangeColorEachNote(strip)
#        pianoColorRainbow(strip)
#        pianoChangeColorRainbowAllSame(strip, 0)

      except KeyboardInterrupt:
          if args.clear:
            colorWipe(strip, Color(0,0,0), 1)
          exit()
      except OSError:
          colorWipe(strip, Color(0,0,0), 1)
          time.sleep(1)
          sys.stdout.flush()
          os.execv(sys.argv[0], sys.argv)
      except IOError:
          colorWipe(strip, Color(0,0,0), 1)
          time.sleep(1)
          sys.stdout.flush()
          os.execv(sys.argv[0], sys.argv)
