import random
from paho.mqtt import client as mqtt_client
import json
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import time

#declares 16 channels
kit = ServoKit(channels=16)

# defines and initializes an empty array to hold the evening pills
evening_pills = []

#defines the evening class to make evening_pill objects with 6 properties 
class Evening:
    def __init__(self, Ename: str, Econtainer: str, Edosage: int, Equantity: int, Edescription: str):
        self.Ename = Ename
        self.Econtainer = Econtainer
        self.Edosage = Edosage
        self.Equantity = Equantity
        self.Echannel = None
        self.Edescription = Edescription

#keeps track of number of scans
scanCount = 0
#variables representing pill information -- used later to create pill objects
name = None
description = None
dosage = None
frequency = None
current_color = None
quantity = None
# ------------------------------------------------MQTT information for broker
broker = 'mqtt.things.ph' #INPUT BROKER NAME
port = 1883
topic = "pibot" #INPUT TOPIC NAME

# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'

username = '66b49ce0c762db171066c05a' #INPUT USERNAME
password = 'A1Zhqr0MKXUz7GXdCRAx5FVD' #INPUT PASSWORD

#---------------------------------- Connects the rasberry pi to the broker
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


#--------------------------------------Subscribes to messages published on the topic
def subscribe(client: mqtt_client):
    #----------Deals with the message received 
    def on_message(client, userdata, msg):
        global description, dosage, frequency, quantity, name, scanCount
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        #Identifies a scan has just occured, increments by 1
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
        print(frequency)
        print(current_color)
        print(quantity)
 
        #checks if there has been less or more than 4 scans
        if scanCount < 3:
            #creates a pill object
            process_med_info(name, current_color, description, dosage, quantity, frequency, evening_pills)
        else:
            #clears out the list of pill objects
            evening_pills.clear()
            #sets the scanCount back to 0
            scanCount = 0
            #creates a pill object
            process_med_info(name, current_color, description, dosage, quantity, frequency, evening_pills)
            
    client.subscribe(topic)
    client.on_message = on_message



#-------------- FUNCTIONS TO ||CREATE THE PILL OBJECTS|| INTO THE EVENING_PILLS LIST AND DO ||MOTOR ASSIGNMENT|| BASED OF COLOR OF CONTAINER


def process_med_info(name, current_color, description, dosage, quantity, frequency, evening_pills): 
    if frequency.lower() == "daily" or frequency.lower() == "everyday" or frequency.lower() == "once":
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

#--------------------!!!!----MAY NEED TO CALL WITH PARAMETER: (EVENING_PILLS)------!!!
def set_servos():
    for i in range(len(evening_pills)):
        if evening_pills[i].Econtainer == "blue":
            evening_pills[i].Echannel = kit.continuous_servo[0]
        elif evening_pills[i].Econtainer == "red":
            evening_pills[i].Echannel = kit.continuous_servo[4]
        elif evening_pills[i].Econtainer == "green":
            evening_pills[i].Echannel = kit.continuous_servo[8]
        elif evening_pills[i].Econtainer == "yellow":
            evening_pills[i].Echannel = kit.continuous_servo[12]
    #PRINTS OUT AND CHECKS IF THE MOTORS HAVE BEEN ASSIGNED ACCORDINGLY
    for pill in evening_pills:
        print(f"Container: {pill.Econtainer}, GPIO Pin: {pill.Echannel}")
        
        

#--------------------------------------------- CODE TO RUN THE DISPENSER


# Set the GPIO mode to BCM 
GPIO.setmode(GPIO.BCM)

#THE MOTORS SHOULD NOT BE SPINNING WHEN THE CODE IS FIRST RUN !!!----MAY NEED TO BE CALLED IN A DIFFERENT LOCATION----!!!
kit.continuous_servo[0].throttle = 0
kit.continuous_servo[4].throttle = 0
kit.continuous_servo[8].throttle = 0
kit.continuous_servo[12].throttle = 0

#DECLARES GLOBAL VARIABLE "BUZZ"
global Buzz 

# SETTING GPIO PIN NUMBERS FOR THE LED, BUZZER, AND ALL THE SENSORS
led_pin = 19
Buzzer = 21
# all four sensors
SENSOR_PIN1 = 4
SENSOR_PIN2 = 17
SENSOR_PIN3 = 22
SENSOR_PIN4 = 18

# -----------------------------SETS THE GPIO PINS AS AN INPUT OR OUTPUT
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(Buzzer, GPIO.OUT) 
GPIO.setup(SENSOR_PIN1, GPIO.IN)
GPIO.setup(SENSOR_PIN2, GPIO.IN)
GPIO.setup(SENSOR_PIN3, GPIO.IN)
GPIO.setup(SENSOR_PIN4, GPIO.IN)


# VARIABLE TO TRACK THE STATE OF THE PHOTOELECTRIC SENSOR
prev_obstacle_state = GPIO.HIGH  # Assuming no obstacle initially (FIGURE OUT IF THIS IS THE CORRECT SETTING)


#----------------------------!!!---FUNCTION THAT DISPENSES PILLS USING SERVOS AND PHOTO SENSORS---!!! VERY IMPORTANT (FIX IMMEDIATELY)
def pillOut(index, duration):
    # Set the servo to the desired throttle (-1 to 1)
    evening_pills[index].Echannel.throttle = 0.2
    #Wait for the specified duration
    time.sleep(1)
    evening_pills[index].Echannel.throttle = -0.2
    time.sleep(1)
    evening_pills[index].Echannel.throttle = 0.2
    time.sleep(1)
    evening_pills[index].Echannel.throttle = -0.2
    time.sleep(1)

    global prev_obstacle_state
    
    while True: # !!!! MAY LOOP FOREVER ---- WATCH OUT !!!!
        
        # INTEGRATE ALL FOUR SENSORS
        obstacle_state1 = GPIO.input(SENSOR_PIN1)
        obstacle_state2 = GPIO.input(SENSOR_PIN2)
        obstacle_state3 = GPIO.input(SENSOR_PIN3)
        obstacle_state4 = GPIO.input(SENSOR_PIN4)

        if obstacle_state1 == prev_obstacle_state and obstacle_state2 and prev_obstacle_state and obstacle_state3 == prev_obstacle_state and obstacle_state4 == prev_obstacle_state:
            if obstacle_state1 != GPIO.LOW or obstacle_state2 != GPIO.LOW or obstacle_state3 != GPIO.LOW or obstacle_state4 != GPIO.LOW:
                evening_pills[index].Echannel.throttle = 0.2 #SLOW SPEED
                print("pill hasn't dropped")
            else:
                print("An obstacle is detected")
                evening_pills[index].Echannel.throttle = 0
                return True #SHOULD EXIT OUT OF LOOP
                

# SETS THE BUZZER FREQUENCY AND SETS THE LED TO OFF
Buzz = GPIO.PWM(Buzzer, 1000)
GPIO.output(led_pin, GPIO.LOW)


try:
        #THIS IS THE FIRST THING THAT SHOULD RUN ALWAYS. PRESCRIPTION TRANSFER BEFORE DISPENSING
     
        for i in range(len(evening_pills)):
            print(evening_pills[i].Econtainer)
            for j in range(evening_pills[i].Edosage):
                #GUI SWITCHES TO DISPENSING SCREEN
                print(str(evening_pills[i].Edosage) + " pills dispensing")
                pillOut(i, 0.2)
                #call function that displays the alert for the pill (with parameters)
            print("end of loop/next pill dispensing")
            time.sleep(2)
            #switch back to default screen or screen that says take your pills. maybe motion sensor code???
     
     
        client = connect_mqtt()
        subscribe(client)
        client.loop_forever()
        time.sleep(20)
      
        print("message recieved -- ready to sound alarm")
        
        for pill in evening_pills:
            print(pill)

        #GUI IS STREAK SCREEN
        #two minute timer until the dispensing starts
        #time.sleep(3)

        #GUI SWITCHES TO READY TO DISPENSE SCREEN AND ALARMS ARE ON FOR FIVE SECONDS
        print("Ready to Dispense!")
        GPIO.output(led_pin, GPIO.HIGH)
        Buzz.start(20)
        time.sleep(5)
    
        print("alarm is done--time to dispense")
        GPIO.output(led_pin, GPIO.LOW)
        Buzz.stop()
        
        print("done?")
             
            
            
finally:
    GPIO.cleanup()
