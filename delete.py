
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

# def setup(Rpin):
# 	global pins
# 	global p_R
# 	pins = {'pin_R': Rpin}     
# 	for i in pins:
# 		GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
# 		GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led
# 	p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
# 
# def map(x, in_min, in_max, out_min, out_max):
# 	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# def off():
# 	for i in pins:
# 		GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
# 		GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds
# # 
# def setColor(col):   # For example : col = 0x112233
# 	R_val = (col & 0xff0000) >> 16
# 	R_val = map(R_val, 0, 255, 0, 100)
# 	p_R.ChangeDutyCycle(100-R_val)     # Change duty cycle



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
