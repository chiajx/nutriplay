## This code was written for Critical Making Provocation 2, last updated April 2, 2018 by JXC with lots of help from KJ in the invention lab, and some help from Mitchell. This script runs on the raspberry pi, with barcode scanner attached. 

## import things that we need

# for the barcode scanner
import sys

# for the LEDs
import time
from time import sleep
from neopixel import *


# LED strip configuration:
LED_COUNT   = 10      # Number of LED pixels
LED_PIN     = 18      # GPIO pin connected to the pixels
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)


#soft variables
good_count = 0
scan_result = 0


## Define functions

# function for the barcode scanner
def barcode_reader():
    """Barcode code obtained from 'brechmos'
    https://www.raspberrypi.org/forums/viewtopic.php?f=45&t=55100"""
    hid = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm',
           17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',
           29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ',
           45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';', 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'}

    hid2 = {4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M',
            17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y',
            29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ',
            45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':', 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'}

    fp = open('/dev/hidraw0', 'rb')
    print("successful barcode library setup")

    ss = ""
    shift = False

    done = False

    while not done:

        ## Get the character from the HID
        buffer = fp.read(8)
        for c in buffer:
            if ord(c) > 0:

                ##  40 is carriage return which signifies
                ##  we are done looking for characters
                if int(ord(c)) == 40:
                    done = True
                    break;

                ##  If we are shifted then we have to
                ##  use the hid2 characters.
                if shift:

                    ## If it is a '2' then it is the shift key
                    if int(ord(c)) == 2:
                        shift = True

                    ## if not a 2 then lookup the mapping
                    else:
                        ss += hid2[int(ord(c))]
                        shift = False

               ##  If we are not shifted then use
                ##  the hid characters

                else:

                    ## If it is a '2' then it is the shift key
                    if int(ord(c)) == 2:
                        shift = True

                    ## if not a 2 then lookup the mapping
                    else:
                        print("ss:"+ss)
                        print("c:"+c)
                        ss += hid[int(ord(c))]
    return ss

# functions for the LEDs
def number():
    global good_count
    good_count += 1
    print(good_count)

def startup(strip, StrobeCount, FlashDelay, EndPause, iterations):
    """Flashes green lights"""
    for j in range(iterations):
        for i in range(StrobeCount):
            for k in range(LED_COUNT):
                strip.setPixelColor(k, Color(255, 0, 0))
            strip.show()
            time.sleep(FlashDelay/1000.0) 
            for k in range(LED_COUNT):
                strip.setPixelColor(k, Color(0, 0, 0))
            strip.show()
            time.sleep(FlashDelay/1000.0)  
        time.sleep(EndPause)


def flash(strip, StrobeCount, FlashDelay, EndPause, iterations):
    """Flashes red lights"""
    for j in range(iterations):
        for i in range(StrobeCount):
            for k in range(LED_COUNT):
                strip.setPixelColor(k, Color(0, 255, 0))
            strip.show()
            time.sleep(FlashDelay/1000.0) 
            for k in range(LED_COUNT):
                strip.setPixelColor(k, Color(0, 0, 0))
            strip.show()
            time.sleep(FlashDelay/1000.0)  
        time.sleep(EndPause)

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
	strip.show()
	time.sleep(wait_ms/1000.0)

def progress(strip, color):
    """Turns on LEDs in progress bar"""
    for i in range(good_count):
	strip.setPixelColor(i, color)
    strip.show()

def reset(strip, color):
    for i in range(LED_COUNT):
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

def theaterChaseRainbow(strip, wait_ms=100): 
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

# Create NeoPixel object
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)

# set up TCP connection
import socket

TCP_IP = '192.168.1.101'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))


### SCRIPT ###

print 'Press Ctrl-C to quit.'
while True:

## insert code to compare barcode to database, output set output = "good" or "bad"

## code for lights

# Intialize the library 
    strip.begin()
    reset(strip, Color(0,0,0))
    if __name__ == '__main__':
        try:
            while True:
                s.send(barcode_reader())
                scan_result = int(s.recv(BUFFER_SIZE))
                print "received data", scan_result

                if scan_result == 1: #result is good
                    print("cood_count: "+str(good_count))

                    if good_count >=9:
                        #while True:
                        for i in range(2):    
                            theaterChaseRainbow(strip)
                        
                        # insert servo code here
                                       
                    else: 
                        # Green wipe twice
                        for i in range(2):
                            colorWipe(strip, Color(255, 0, 0))
                            colorWipe(strip, Color(0, 0, 0)) 
               
                        # update the counter
                        good_count += 1
                        print("Number of good items collected: "
                              + str(good_count))
                        # Update the progress bar
                        progress(strip, Color(255,0,0))
             

                elif scan_result == 3: #initialize
                    startup(strip,3, 1000, 1, 2)
                    colorWipe(strip, Color(255, 0, 0))
                    colorWipe(strip, Color(0, 0, 0))

                    good_count = 0


                else: #result is bad

                    flash(strip, 5, 100, 1, 2) # Flash red lights for 'bad' item scanned
                    print("bad item!")

                    progress(strip, Color(255,0,0))
        except KeyboardInterrupt:
            pass
            s.close()


