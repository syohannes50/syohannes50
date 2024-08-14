import random
from paho.mqtt import client as mqtt_client
import json
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import time
import tkinter
import customtkinter as ctk


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

#---------------------------------- Connects the Rasberry Pi to the broker and Exits
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


#--------------------------------------Subscribes to messages published on the topic and Exits
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
            
    #------------------EXIT OUT OF THIS FUNCTION!!!!!!!!
   
    client.subscribe(topic)
    client.on_message = on_message
    #waiting 30 seconds for person to scan
    time.sleep(30) #MAY HAVE TO MOVE THIS DEPENDING ON HOW CODE RESPONDS
    print("Exiting out of subscribe...")
    return True



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
        print(f"Container: {pill.Econtainer}, Servo Channel: {pill.Echannel}")
        
        

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
def pillOut(index):
    # Set the servo to the desired throttle (-1 to 1)
    evening_pills[index].Echannel.throttle = 1
    #Wait for the specified duration
    time.sleep(0.25)
    evening_pills[index].Echannel.throttle = -1
    time.sleep(0.25)
    evening_pills[index].Echannel.throttle = 1
    time.sleep(0.25)
    evening_pills[index].Echannel.throttle = -1
    time.sleep(0.25)
    print("Shook the container!")

    global prev_obstacle_state
    
    while True: # !!!! MAY LOOP FOREVER ---- WATCH OUT !!!!
        print("Starting while loop!")
        # INTEGRATE ALL FOUR SENSORS
        obstacle_state1 = GPIO.input(SENSOR_PIN1)
        obstacle_state2 = GPIO.input(SENSOR_PIN2)
        obstacle_state3 = GPIO.input(SENSOR_PIN3)
        obstacle_state4 = GPIO.input(SENSOR_PIN4)
        
        #CHECKS IF ALL THE PHOTELECTRIC SENSORS AREN'T DETECTING ANYTHING (A.K.A. PILLS) !!!--MAYBE DO 'AND' INSTEAD OF 'OR' FOR MAX SAFETY--!!!!
        if obstacle_state1 == prev_obstacle_state or obstacle_state2 or prev_obstacle_state or obstacle_state3 == prev_obstacle_state or obstacle_state4 == prev_obstacle_state:
            print("Checked for pills!")
            if obstacle_state1 != GPIO.LOW or obstacle_state2 != GPIO.LOW or obstacle_state3 != GPIO.LOW or obstacle_state4 != GPIO.LOW:
                #MAY PUT THIS UNDER FIRST IF-STATEMENT OR OUTSIDE OF THE IF-STATEMENTS
                evening_pills[index].Echannel.throttle = 0.2 #SLOW SPEED
                print("pill hasn't dropped")
            else:
                print("An obstacle is detected")
                evening_pills[index].Echannel.throttle = 0
                print("Stopped spinning container")
                print("Exiting out of while loop....")
                return True #SHOULD EXIT OUT OF LOOP
                

# SETS THE BUZZER FREQUENCY AND SETS THE LED TO OFF
Buzz = GPIO.PWM(Buzzer, 1000)
GPIO.output(led_pin, GPIO.LOW)

#SOMEWHERE UP HERE, SET UP STREAK SCREEN AND DEFINE ALL THE FRAMES, BUTTONS, AND FUNCTIONS

#----------------------------------------------------------STREAKFRAME
streakframe = ctk.CTkFrame (window,
                           width = 800,
                           height = 480)

streak = ctk.CTkLabel(streakframe,
                      width = 800,
                      height = 500,
                      text = "You're on a \n [] day streak!",
                      font = ('Sans-Serif', 40, 'bold')),
                      fg_color = '#ffb9d5'
streak.place(relx=0.35, rely=0.5, anchor=tkinter.CENTER)

streakframe.pack(padx=5, pady=5)
streakframe.pack_propagate(False)
#------------------------------------------------------------READY FRAME 
readyframe = ctk.CTkFrame (window,
                           width = 800,
                           height = 480)
readyframe.pack(padx=5, pady=5)
readyframe.pack_propagate(False)
label1 = ctk.CTkLabel(readyframe,
                      width = 800,
                      height = 500,
                      text = "It's time to take your medication",
                      text_color = 'black',
                      font = ('Sans-Serif', 35, 'bold'),
                      fg_color = '#ffb9d5')
label1.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

#-------------------------------------------------------------DISPENSE FRAME 
dispenseframe = ctk.CTkFrame (window,
                              width = 800,
                              height = 480)
dispenseframe.pack(padx=5, pady=5)
dispenseframe.pack_propagate(False)
label2 = ctk.CTkLabel(dispenseframe,
                      width = 800,
                      height = 500,
                      text = "Dispensing...",
                      text_color = 'black',
                      font = ('Sans-Serif', 40, 'bold'),
                      fg_color = '#ffb9d5')
label2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
#-----------------------------------------------------------DAYS LEFT FRAME 

daysframe = ctk.CTkFrame (window,
                           width = 800,
                           height = 480)
daysframe.pack(padx=5, pady=5)
daysframe.pack_propagate(False)
label3 = ctk.CTkLabel(readyframe,
                      width = 800,
                      height = 500,
                      text = "You have 10 day(s) of Cymbalta left", #days = variable 
                      text_color = 'black',
                      font = ('Sans-Serif', 35, 'bold'),
                      fg_color = '#ffb9d5')
label3.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

hello = ctk.CTkLabel(readyframe,
                  width = 800,
                  height = 80,
                  text = "Hi, PillPal User",
                  fg_color = '#ffff9c',
                  text_color = 'black',
                  font = ('Sans-Serif', 30, 'bold'))
hello.pack(padx=10, pady=10)

pages = [streakframe, readyframe, dispenseframe, daysframe]
count = 0

#-------------------------------------------------------------NEXT PAGE FUNCTION
def next_page():
    global count
    global pages  # Ensure pages is declared as a global variable if used elsewhere

    if count < len(pages) - 1:
        # Hide all pages
        for p in pages:
            p.pack_forget()
        
        # Increment the page index
        count += 1

        # Show the new page
        page = pages[count]
        page.pack(padx=5, pady=5)
    else:
        print("You are already on the last page.")
#-------------------------------------------------------- SHOW PAGE FUNCTION
def show_page(index):
    for i, page in enumerate(pages):
        if i == index:
            page.pack(fill='both', expand=True)  # Show the frame
        else:
            page.pack_forget()  # Hide all other frames

#--------------------------------------------------- DISPENSE NOW BUTTON
button1 = ctk.CTkButton(readyframe,
                        text="Dispense Now",
                        text_color='black',
                        font = ('Sans-Serif', 20, 'bold'),
                        width=300,
                        height=75,
                        fg_color='#ff78ae',
                        border_width=5,
                        border_color='red',
                        hover_color='red',
                        command=next_page)
button1.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)
#------------------------------------------------------- STREAKFRAME TO READYFRAME BUTTON
button2 = ctk.CTkButton(streakframe,
                        text="next",
                        text_color='black',
                        font = ('Sans-Serif', 20, 'bold'),
                        width=300,
                        height=75,
                        fg_color='#ff78ae',
                        border_width=5,
                        border_color='red',
                        hover_color='red',
                        command=next_page)
button2.place(relx=0.5, rely=0.80, anchor=tkinter.CENTER)
#------------------------------------------------------- STREAKFRAME TO READYFRAME BUTTON
button3 = ctk.CTkButton(dispenseframe,
                        text="next",
                        text_color='black',
                        font = ('Sans-Serif', 20, 'bold'),
                        width=300,
                        height=75,
                        fg_color='#ff78ae',
                        border_width=5,
                        border_color='red',
                        hover_color='red',
                        command=next_page)
button3.place(relx=0.5, rely=0.80, anchor=tkinter.CENTER)

window.mainloop()


try:
        #!!!-----PUT IN A TIME.SLEEP() SOMEWHERE TO ACT AS A TIMER FOR HOW LONG IT TAKES TO SCAN A PRESCRIPTION------!!!
        count = 0
        show_page(count)
        #FIRST: MQTT CONNECTION & APP TO RASPI INFO TRANSFER
        client = connect_mqtt()
        subscribe(client)
        print("Exit out of subscribe complete") #MAY NEED TO MOVE THIS FOR TESTING PURPOSES
        client.loop_forever() #MAY NOT NEED TO BE HERE: FIND OTHER PLACE FOR IT

        #SECOND: EXIT OUT OF MQTT LOOP
        print("Message recieved -- Ready to sound alarm!")
    
        #THIRD: SET THE PILL OBJETS TO THE SERVOS & PRINT TO CHECK IF THE PILL OBJECTS ARE THERE BEFORE DISPENSING
        set_servos()
        print("Assigned the pill objects to servos!")
        # Hesitant about this for loop
        for pill in evening_pills:
            print(pill)

        count = 1
        show_page(count)
        #FOURTH: SOUND THE ALARM, TURN ON LED
        #DISPLAY READYFRAME ON GUI
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
                count = 2
                show_page(count)
                #GUI SWITCHES TO DISPENSING SCREEN
                print(str(evening_pills[i].Edosage) + " pills dispensing")
                print("calling pillOut")
                pillOut(i)
                print("Exit completed. Next pill is dispensing...")
                count = 3
                show_page(count)
                #CALL FUNCTION THAT DISPLAYS THE DAYS LEFT FRAME (WITH PARAMETERS TO ACCESS DATA)
            print("Next container is dispensing...")
            time.sleep(1)
            
        print("Finished Dispensing!") 
        count = 0
        show_page(count)
        #SWITCH BACK TO STREAK SCREEN
            
finally:
    GPIO.cleanup()
