#! /usr/bin/env python

# Simple clock program. Writes the exact time.
# Demo program for the I2C 16x2 Display from Ryanteck.uk
# Created by Matthew Timmons-Brown for The Raspberry Pi Guy YouTube channel

# Import necessary libraries for communication and display use
import drivers
from time import sleep
from datetime import datetime
import Adafruit_DHT
DHT = 4

# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = drivers.Lcd()

try:
    print("Writing to display")
    display.lcd_display_string("  Temp. & Humidity", 1)  # Write line of text to first line of display
    while True:
        h,t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT)
        #display.lcd_display_string(str(datetime.now().date()), 4)
        # Write just the time to the display
        display.lcd_display_string(str(' T={0:0.1f}*C   H={1:0.1f}%'.format(t,h)), 2)
# Uncomment the following line to loop with 1 sec delay
        #Read Temp and Hum from DHT22
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
    display.lcd_display_string(" Resetting Display", 2)
    sleep(1)
    display.lcd_clear()

