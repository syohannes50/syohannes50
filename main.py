import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

    # Define the evening_pills list
evening_pills = []

class Evening:
    def __init__(self, Ename: str, Econtainer: str, Edosage: int, Equantity: int, Edescription: str):
        self.Ename = Ename
        self.Econtainer = Econtainer
        self.Edosage = Edosage
        self.Equantity = Equantity
        self.Echannel = None
        self.Edescription = Edescription

  
    def process_med_info(name, current_color, description, dosage, quantity, frequency, evening_pills): #remove evening_pills as a parameter
    if frequency.lower() == "daily":
        if _description.lower() == "with food":
            # Instantiate new Evening medicine
            pill = Evening(Ename=name, Econtainer=current_color, Edescription=description, Edosage=dosage, Equantity=quantity)
            evening_pills.append(epill)
            print("New Evening Pill Added:")
            print(f"Name: {pill.Ename}, Container: {pill.Econtainer}, Description: {pill.Edescription}, Dosage: {pill.Edosage}, Quantity: {pill.Equantity}")
    else:
        # Instantiate new Evening medicine
        pill = Evening(Ename=name, Econtainer=current_color, Edescription=description, Edosage=dosage, Equantity=quantity)
        evening_pills.append(pill)
        print("New Evening Pill Added:")
        print(f"Name: {pill.Ename}, Container: {pill.Econtainer}, Description: {pill.Edescription}, Dosage: {pill.Edosage}, Quantity: {pill.Equantity}")


# Adding a evening pill object to the list
evening_pills.append(Evening(Econtainer="yellow", Edosage=1, Equantity=0, Edescription="with food"))
evening_pills.append(Evening(Econtainer="green", Edosage=2, Equantity=0, Edescription="without food"))


for i in range(len(evening_pills)):
    if evening_pills[i].Econtainer == "blue":
        evening_pills[i].Echannel = kit.continuous_servo[0]
    elif evening_pills[i].Econtainer == "red":
        evening_pills[i].Echannel = kit.continuous_servo[2]
    elif evening_pills[i].Econtainer == "green":
        evening_pills[i].Echannel = kit.continuous_servo[4]
    elif evening_pills[i].Econtainer == "yellow":
        evening_pills[i].Echannel = kit.continuous_servo[6]
        
        
for pill in evening_pills:
    print(f"Container: {pill.Econtainer}, GPIO Pin: {pill.Echannel}")
    

# Set the GPIO mode to BCM (Broadcom SOC channel numbering)
GPIO.setmode(GPIO.BCM)

#motor isn't moving at first
# kit.continuous_servo[0].throttle = 0
# kit.continuous_servo[2].throttle = 0
kit.continuous_servo[4].throttle = 0
kit.continuous_servo[6].throttle = 0


# Set the pin number connected to the ir obstacle avoidance sensor
switch_pin = 17
led_pin = 13
Buzzer = 12
# all four sensors and the pins
SENSOR_PIN1 = 18
SENSOR_PIN2 = 21
# SENSOR_PIN3 = 
# SENSOR_PIN4 = 

global Buzz 

# Set the GPIO pin as an input
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(Buzzer, GPIO.OUT) 
GPIO.setup(SENSOR_PIN1, GPIO.IN)
GPIO.setup(SENSOR_PIN2, GPIO.IN)


# Variable to track the obstacle avoidance sensor state
prev_obstacle_state = GPIO.HIGH  # Assuming no obstacle initially

def printReady():
    print("ready")

def photoelectric_sensor_detects_pill():
    
    global prev_obstacle_state
    
    while True:
        # works for all four sensors
        obstacle_state1 = GPIO.input(SENSOR_PIN1)
        obstacle_state2 = GPIO.input(SENSOR_PIN2)
        if obstacle_state1 != prev_obstacle_state or obstacle_state2 != prev_obstacle_state:
            if obstacle_state1 == GPIO.LOW or obstacle_state2 == GPIO.LOW:
                print("An obstacle is detected")
                kit.continuous_servo[6].throttle = 0
                kit.continuous_servo[4].throttle = 0
                return True
            else:
                print("An obstacle is removed")
                

Buzz = GPIO.PWM(Buzzer, 1000)

GPIO.output(led_pin, GPIO.LOW)

try:
        
        if GPIO.input(switch_pin) == GPIO.HIGH:
            print("Ready to Dispense!")
            Buzz.start(20)
            GPIO.output(led_pin, GPIO.HIGH)
            time.sleep(5)
        if GPIO.input(switch_pin) == GPIO.LOW:
            GPIO.output(led_pin, GPIO.LOW)
            Buzz.stop() 
            
            # once the switch is off, run loop to dispense all the evening pills
            for i in range(len(evening_pills)):
                print(evening_pills[i].Econtainer)
                for j in range(evening_pills[i].Edosage):
                    print(str(evening_pills[i].Edosage) + " pills dispensing")
                    evening_pills[i].Echannel.throttle = 0.2
                    time.sleep(3)
                    printReady()
                    photoelectric_sensor_detects_pill()
                    print("restarting loop")




finally:
    GPIO.cleanup()
