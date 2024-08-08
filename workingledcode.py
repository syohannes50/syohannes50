
import RPi.GPIO as GPIO
# from adafruit_servokit import ServoKit
import time

# kit = ServoKit(channels=16)

colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]
R = 23                                                                      

# Set the GPIO mode to BCM (Broadcom SOC channel numbering)
GPIO.setmode(GPIO.BCM)

# Set the pin number connected to the ir obstacle avoidance sensor
switch_pin = 17
Buzzer = 12

# Set the GPIO pin as an input
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Buzzer, GPIO.OUT)
GPIO.setup(R, GPIO.OUT)
                
global Buzz

Buzz = GPIO.PWM(Buzzer, 1000)

def loop(cond):
    if (cond == 1):
        GPIO.output(R, GPIO.HIGH)
        time.sleep(3)
    else:
       GPIO.output(R, GPIO.LOW) 


try:
        
        if GPIO.input(switch_pin) == GPIO.HIGH:
            print("Ready to Dispense!")
            #set high
            loop(1)
            time.sleep(3)
            Buzz.start(60)
            time.sleep(3)
            
        if GPIO.input(switch_pin) == GPIO.LOW:
            print("Dispensing")
            loop(2)
            Buzz.stop()
            #set low
            


finally:
    GPIO.cleanup()
