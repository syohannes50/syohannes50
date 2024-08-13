import random
from paho.mqtt import client as mqtt_client
import json
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import time

evening_pills = []

class Evening:
    def __init__(self, Ename: str, Econtainer: str, Edosage: int, Equantity: int, Edescription: str):
        self.Ename = Ename
        self.Econtainer = Econtainer
        self.Edosage = Edosage
        self.Equantity = Equantity
        self.Echannel = None
        self.Edescription = Edescription


scanCount = 0

description = None
dosage = None
frequency = None
current_color = None
name = None
quantity = None

broker = 'mqtt.things.ph' #INPUT BROKER NAME
port = 1883
topic = "pibot" #INPUT TOPIC NAME

# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'

username = '66b49ce0c762db171066c05a' #INPUT USERNAME
password = 'A1Zhqr0MKXUz7GXdCRAx5FVD' #INPUT PASSWORD


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port) 
    return client


#Prints the recieved message
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global description, dosage, frequency, quantity, name, scanCount
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        scanCount += 1
        
        # Decode the incoming JSON data
        data = json.loads(msg.payload.decode())
            
        # Store the received data in the corresponding variables
        description = data.get("description")
        dosage = data.get("dosage")
        quantity = data.get("quantity")
        name = data.get("name")
        frequency = data.get("frequency")
        current_color = data.get("currentColor")
            
            
        print(name)
        print(description)
        print(dosage)
        print(quantity)
        print(frequency)
        print(current_color)
            
 
        
        if scanCount < 3:
            process_med_info(name, current_color, description, dosage, quantity, frequency, evening_pills)
        else:
            evening_pills.clear()
            scanCount = 0
            
    client.subscribe(topic)
    client.on_message = on_message



#------------------------------------------- HANDLES THE EVENING PILLS LIST AND MOTOR ASSIGNMENT
    # Define the evening_pills list


def process_med_info(name, current_color, description, dosage, quantity, frequency, evening_pills): #remove evening_pills as a parameter
    if frequency.lower() == "daily" or frequency.lower() == "everyday":
        if description.lower() == "with food":
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

'''


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
kit.continuous_servo[0].throttle = 0
kit.continuous_servo[2].throttle = 0
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

def pillOut(index, duration):
    # Set the servo to the desired throttle (-1 to 1)
    evening_pills[index].Echannel.throttle = 0.2
    #Wait for the specified duration
    time.sleep(duration)
    evening_pills[index].Echannel.throttle = -0.2
    time.sleep(duration)
    evening_pills[index].Echannel.throttle = 0.2
    time.sleep(duration)
    evening_pills[index].Echannel.throttle = -0.2
    time.sleep(duration)

    global prev_obstacle_state
    
    while True:
        # integrate all four sensors
        obstacle_state1 = GPIO.input(SENSOR_PIN1)
        obstacle_state2 = GPIO.input(SENSOR_PIN2)

        if obstacle_state1 == prev_obstacle_state or obstacle_state2 == prev_obstacle_state:
            if obstacle_state1 != GPIO.LOW or obstacle_state2 != GPIO.LOW:
                print("pill hasn't dropped")
                evening_pills[index].Echannel.throttle = 0.5
                sleep(duration)
            else:
                print("An obstacle is detected")
                evening_pills[index].Echannel.throttle = 0
                return True


Buzz = GPIO.PWM(Buzzer, 1000)
GPIO.output(led_pin, GPIO.LOW)
'''
try:
        #THIS IS THE FIRST THING THAT SHOULD RUN ALWAYS. PRESCRIPTION TRANSFER BEFORE DISPENSING
        client = connect_mqtt()
        subscribe(client)
        client.loop_forever()
        
        
        '''
        

        #GUI IS STREAK SCREEN
    
        #two minute timer until the dispensing starts
        time.sleep(120)

        #GUI SWITCHES TO READY TO DISPENSE SCREEN AND ALARMS ARE ON FOR FIVE SECONDS
        print("Ready to Dispense!")
        GPIO.output(led_pin, GPIO.HIGH)
        Buzz.start(20)
        time.sleep(5)

        

        #if BUTTON IS CLICKED ON GUI:
            GPIO.output(led_pin, GPIO.LOW)
            Buzz.stop() 
            
            # once the switch is off, run loop to dispense all the evening pills
            for i in range(len(evening_pills)):
                print(evening_pills[i].Econtainer)
                for j in range(evening_pills[i].Edosage):
                    #GUI SWITCHES TO DISPENSING SCREEN
                    print(str(evening_pills[i].Edosage) + " pills dispensing")
                    pillOut(i, 0.2)
                    #call function that displays the alert for the pill (with parameters)
                    print("end of loop/next pill dispensing")
                    time.sleep(2)
            #switch back to default screen or screen that says take your pills. maybe motion sensor code????
'''
finally:
    GPIO.cleanup()
            #switch back to default screen or screen that says take your pills. maybe motion sensor code????

finally:
    GPIO.cleanup()
