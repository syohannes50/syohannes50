import random
from paho.mqtt import client as mqtt_client
import json
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import time

description = None
dosage = None
frequency = None
name = None
quantity = None

broker = 'mqtt.things.ph' #INPUT BROKER NAME
port = 1883
topic = "pibot" #INPUT TOPIC NAME

# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'

username = '66b49ce0c762db171066c05a' #INPUT USERNAME
password = '' #INPUT PASSWORD


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port) // currently don't want to use user/pass
    return client


#Prints the recieved message
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global description, dosage, frequency, quantity, name
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    try:
        # Decode the incoming JSON data
        data = json.loads(msg.payload.decode())
        
        # Store the received data in the corresponding variables
        description = data.get("description")
        dosage = data.get("dosage")
        quantity = data.get("quantity")
        name = data.get("name")
        frequency = data.get("frequency")
        
        
    except:
        print("Error: Failed to decode JSON")
        
            
    client.subscribe(topic)
    client.on_message = on_message



#------------------------------------------- HANDLES THE EVENING PILLS LIST AND MOTOR ASSIGNMENT
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

#--------------------------------------------- CODE TO RUN THE DISPENSER

kit = ServoKit(channels=16)

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
SENSOR_PIN3 = 
SENSOR_PIN4 = 

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
        #THIS IS THE FIRST THING THAT SHOULD RUN ALWAYS. PRESCRIPTION TRANSFER BEFORE DISPENSING
        client = connect_mqtt()
        subscribe(client)
        client.loop_forever()

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