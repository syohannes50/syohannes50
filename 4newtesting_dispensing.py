import random
from paho.mqtt import client as mqtt_client
import json
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import time
import Adafruit_PCA9685 


#declares 16 channels
kit = ServoKit(channels=16)

# defines and initializes an empty array to hold the evening pills
evening_pills = []

#defines the evening class to make evening_pill objects with 6 properties (UPDATE TO 7 FOR GUI)
class Evening:
    def __init__(self, Ename: str, Econtainer: str, Edosage: int, Equantity: int, Edescription: str, Efrequency: str):
        self.Ename = Ename
        self.Econtainer = Econtainer
        self.Edosage = Edosage
        self.Equantity = Equantity
        self.Echannel = None
        self.Edescription = Edescription
        self.Efrequency = Efrequency

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

            #EXIT OUT OF THIS FUNCTION!!!!!!!!


    
    client.subscribe(topic)
    client.on_message = on_message
    #waiting 30 seconds for person to scan
    #MAY HAVE TO MOVE THIS DEPENDING ON HOW CODE RESPONDS
    print("Exiting out of subscribe...")
    return True



#-------------- FUNCTIONS TO ||CREATE THE PILL OBJECTS|| INTO THE EVENING_PILLS LIST AND DO ||MOTOR ASSIGNMENT|| BASED OF COLOR OF CONTAINER

def process_med_info(name, current_color, description, dosage, quantity, frequency, evening_pills): 
    if frequency.lower() == "daily" or frequency.lower() == "everyday" or frequency.lower() == "once":
        if description.lower() == "with food":
            # Instantiate new Evening medicine
            pill = Evening(Ename=name, Econtainer=current_color, Edescription=description, Edosage=dosage, Equantity=quantity, Efrequency = frequency)
            evening_pills.append(epill)
            print("New Evening Pill Added:")
            print(f"Name: {pill.Ename}, Container: {pill.Econtainer}, Description: {pill.Edescription}, Dosage: {pill.Edosage}, Quantity: {pill.Equantity}, Frequency: {pill.Efrequency}")
    else:
        # Instantiate new Evening medicine
        pill = Evening(Ename=name, Econtainer=current_color, Edescription=description, Edosage=dosage, Equantity=quantity, Efrequency = frequency)
        evening_pills.append(epill)
        print("New Evening Pill Added:")
        print(f"Name: {pill.Ename}, Container: {pill.Econtainer}, Description: {pill.Edescription}, Dosage: {pill.Edosage}, Quantity: {pill.Equantity}, Frequency: {pill.Efrequency}")

#--------------------!!!!----MAY NEED TO CALL WITH PARAMETER: (EVENING_PILLS)------!!!
def set_servos():
    for i in range(len(evening_pills)):
        if evening_pills[i].Econtainer == "blue":
            evening_pills[i].Echannel = 0
        elif evening_pills[i].Econtainer == "red":
            evening_pills[i].Echannel = 4
        elif evening_pills[i].Econtainer == "green":
            evening_pills[i].Echannel = 8
        elif evening_pills[i].Econtainer == "purple":
            evening_pills[i].Echannel = 12
    #PRINTS OUT AND CHECKS IF THE MOTORS HAVE BEEN ASSIGNED ACCORDINGLY
    for pill in evening_pills:
        print(f"Container: {pill.Econtainer}, GPIO Pin: {pill.Echannel}")
        
        

#----------------------------------------------------- CODE TO RUN THE DISPENSER



# Create a PCA9685 instance with a specific I2C bus number.
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)  # Replace `1` with your bus number



# Set the PWM frequency to 60Hz, which is common for servos.
pwm.set_pwm_freq(60)
# 
# def set_servo_angle(channel, angle):
#     pulse_width = int((angle / 180.0 * 2000) + 1000)  # Convert angle to pulse width (1000-2000µs)
#     pwm.set_pwm(channel, 0, int(pulse_width * 4096 / 20000))  # Map pulse width to PWM value


#THE MOTORS SHOULD NOT BE SPINNING WHEN THE CODE IS FIRST RUN !!!----MAY NEED TO BE CALLED IN A DIFFERENT LOCATION----!!!

def pulse_width_to_pwm(pulse_width_us):
    return int(pulse_width_us * 4096 / 20000)

def stop_servos():
    neutral_pwm_value = pulse_width_to_pwm(0)  # Typically around 307
    for channel in range(16):
        pwm.set_pwm(channel, 0, neutral_pwm_value)


# Set the GPIO mode to BCM 
GPIO.setmode(GPIO.BCM)

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

# Function to map throttle to PWM with channel as a parameter
def set_throttle(channel, throttle_value):
    global pwm_value
    if throttle_value == 1:
        pwm_value = 409  # Full speed one direction
    elif throttle_value == -1:
        pwm_value = 204  # Full speed opposite direction

    pwm.set_pwm(channel, 0, pwm_value)
  
#SECOND FUNCITON TO CHANGE THROTTLE
def set_throttle2(channel, throttle_value):
    global pwm_value2
    pwm_value2 = int(throttle_value)
    pwm.set_pwm(channel, 0, pwm_value2)

# VARIABLE TO TRACK THE STATE OF THE PHOTOELECTRIC SENSOR
prev_obstacle_state = GPIO.HIGH  # Assuming no obstacle initially (FIGURE OUT IF THIS IS THE CORRECT SETTING)


#----------------------------!!!---FUNCTION THAT DISPENSES PILLS USING SERVOS AND PHOTO SENSORS---!!! VERY IMPORTANT (FIX IMMEDIATELY)
def pillOut(index):

    # Set the servo to the desired throttle 
    set_throttle(evening_pills[index].Echannel, 1)
    #Wait for the specified duration
    time.sleep(0.25)
    set_throttle(evening_pills[index].Echannel, -1)
    time.sleep(0.25)
    set_throttle(evening_pills[index].Echannel, 1)
    time.sleep(0.25)
    set_throttle(evening_pills[index].Echannel, -1)
    time.sleep(0.25)

    print("Shook the container on channel", evening_pills[index].Echannel)

    set_throttle2(evening_pills[index].Echannel, 10)
    global prev_obstacle_state
    print("Starting while loop!")
    while True: # !!!! MAY LOOP FOREVER ---- WATCH OUT !!!!
        
        # INTEGRATE ALL FOUR SENSORS
        obstacle_state1 = GPIO.input(SENSOR_PIN1)
        obstacle_state2 = GPIO.input(SENSOR_PIN2)
        obstacle_state3 = GPIO.input(SENSOR_PIN3)
        obstacle_state4 = GPIO.input(SENSOR_PIN4)

         #SPINNING CONTAINER ON SLOW SPEED
        
        #CHECKS IF ALL THE PHOTELECTRIC SENSORS ARE DETECTING ANYTHING (A.K.A. PILLS) 
        if obstacle_state1 != prev_obstacle_state or obstacle_state2 != prev_obstacle_state or obstacle_state3 != prev_obstacle_state or obstacle_state4 != prev_obstacle_state:
            print("Checked if pills dropped")
            if obstacle_state1 == GPIO.LOW or obstacle_state2 == GPIO.LOW or obstacle_state3 == GPIO.LOW or obstacle_state4 == GPIO.LOW:
                print("An obstacle is detected -- Pill has dropped")
                set_throttle2(evening_pills[index].Echannel, 0) #SLOW SPEED
                print("Exiting out of pillOut..")
                return True
            else:
                print("An obstacle is removed")
                

# SETS THE BUZZER FREQUENCY AND SETS THE LED TO OFF
Buzz = GPIO.PWM(Buzzer, 1000)
GPIO.output(led_pin, GPIO.LOW)

#SOMEWHERE UP HERE, SET UP STREAK SCREEN AND DEFINE ALL THE FRAMES, BUTTONS, AND FUNCTIONS

# -----------------------------------ADDING THREE EVENING PILL OBJECTS TO THE LIST
evening_pills.append(Evening(Ename="pill1", Econtainer="blue", Edosage=1, Equantity=10, Edescription="with food", Efrequency ="twice"))
evening_pills.append(Evening(Ename="pill2", Econtainer="red", Edosage=1, Equantity=20, Edescription="with food", Efrequency ="twice"))
evening_pills.append(Evening(Ename="pill3", Econtainer="green", Edosage=2, Equantity=30, Edescription="with food", Efrequency ="twice"))


try:
        #PUT IN A TIME.SLEEP() SOMEWHERE TO ACT AS A TIMER FOR HOW LONG IT TAKES TO SCAN A PRESCRIPTION
        #SERVOS DON'T MOVE AT FIRST
        stop_servos()
        
        #FIRST: MQTT CONNECTION & APP TO RASPI INFO TRANSFER
        client = connect_mqtt()
        subscribe(client)
        print("Exit out of subscribe complete") #MAY NEED TO MOVE THIS FOR TESTING PURPOSES
        client.loop_start() #LOOP_START() RUNS MESSAGING IT ON A BACKGROUND THREAD || CAN EXECUTE CODE BELOW
        time.sleep(10)
        #THIRD: SET THE PILL OBJETS TO THE SERVOS
        set_servos()
        print("Assigned the pill objects to servos!")

        #FOURTH: SOUND THE ALARM, TURN ON LED, AND DISPLAY READYFRAME ON GUI
        print("Ready to Dispense!")
        GPIO.output(led_pin, GPIO.HIGH)
        Buzz.start(20)
        #INSTEAD OF TIMER DO CONDITIONALS WITH THE GUI FRAMES AND BUTTON (EX: IF BUTTON IS CLICKED CALL FUNCTION TO MOVE ON TO DISPENSING)
        time.sleep(5)

        #FIFTH: TURN OFF LED AND BUZZER, DISPENSE THE PILLS!!!
        print("Alarm has sounded -- Time to dispense!")
        GPIO.output(led_pin, GPIO.LOW)
        Buzz.stop()
    
        for i in range(len(evening_pills)):
            print(evening_pills[i].Econtainer + " dispensing")
            for j in range(evening_pills[i].Edosage):
                #GUI SWITCHES TO DISPENSING SCREEN
                print(str(evening_pills[i].Edosage) + " pills dispensing")
                print("Calling pillOut(), dispensing has started.")
                pillOut(i)
                print("Exit completed. Next pill is dispensing...")
                #CALL FUNCTION THAT DISPLAYS THE DAYS LEFT FRAME (WITH PARAMETERS TO ACCESS DATA)
            print("Next container is dispensing...")
            time.sleep(1)
            
        print("Finished Dispensing!") 
        #SWITCH BACK TO STREAK SCREEN
            
finally:
    GPIO.cleanup()
