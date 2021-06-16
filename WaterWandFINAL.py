#! /usr/bin/env python

# Import necessary libraries for communication and display use
import drivers
from time import sleep
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
from uFire_EC import uFire_EC

DHT = 4
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define GPIO to use on Pi
GPIO_TRIGGER = 22
GPIO_ECHO    = 27

# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = drivers.Lcd()
# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

try:
    print("Writing to display")
    print ("Ultrasonic Measurement")
    print ("Taking EC measurement")
    while True:
        display.lcd_display_string("  Temp. & Humidity", 1)
        h,t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT)
        #display.lcd_display_string(str(datetime.now().date()), 4)
        # Write just the time to the display
        display.lcd_display_string(str('   T={0:0.1f}*C  H={1:0.1f}%'.format(t,h)), 2)
        ec = uFire_EC(i2c_bus=1)
        #ec.reset()
        ecM = ec.measureEC()
        ecF = abs(ecM)
        display.lcd_display_string(str('    EC = {0:0.1f}uS        '.format(ecF)), 3)

    # Allow module to settle
        time.sleep(0.5)

        # Send 10us pulse to trigger
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        start = time.time()

        while GPIO.input(GPIO_ECHO)==0:
          start = time.time()

        while GPIO.input(GPIO_ECHO)==1:
          stop = time.time()

        # Calculate pulse length
        elapsed = stop-start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distancet = elapsed * 34300

        # That was the distance there and back so halve the value
        distance = 93 - (distancet / 2)
        #distance = distancet / 2
        #distanceF = round (distance, 3)
        #print  ("Distance :", distanceF, " cm")
        display.lcd_display_string(str('Water Depth:{0:0.1f}cm   '.format(distance)), 4)

# Uncomment the following line to loop with 1 sec delay
        #Read Temp and Hum from DHT22
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
    display.lcd_display_string(" Resetting Display", 3)
    sleep(1)
    display.lcd_clear()


