import tkinter
import customtkinter as ctk
#----------------------------------------------- CHANGES TO MAIN.PY FOR THE PURPOSE OF THE DISPLAY ---------------------------#

class Evening:
    def __init__(self, Ename: str, Econtainer: str, Edosage: int, Equantity: int, Edescription: str, Efrequency: str):
        self.Ename = Ename
        self.Econtainer = Econtainer
        self.Edosage = Edosage
        self.Equantity = Equantity
        self.Echannel = None
        self.Edescription = Edescription
        self.Efrequency

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
#--------------------------------------------------WILL BE REPLACED BY LAURENS CODE

#theme & color
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

#window size & title
window = ctk.CTk()
window.title('PillPal GUI')
window.geometry("800x480")

#----------------------------------------------------------STREAKFRAME
streakframe = ctk.CTkFrame (window,
                           width = 800,
                           height = 480)

streak = ctk.CTkLabel(streakframe,
                      width = 800,
                      height = 500,
                      text = "You're on a \n {streakCount} day streak!",
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
                      text = "You have {days} day(s) of {name} left", #days = variable 
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
    #set flag to true when button is clicked
    button1_clicked = True
    print("button clicked!")
    
#-------------------------------------------------------- SHOW PAGE FUNCTION (MAYBE REPLACED BY LAURENS CODE)
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
#------------------------------------------------------- STREAKFRAME TO READYFRAME BUTTON (MAY BE DELETED)
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
#------------------------------------------------------- STREAKFRAME TO READYFRAME BUTTON (MAY BE DELETED)
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

#DEFINE GLOBAL VARIABLES
global button1_clicked = False
global name 
global days
global streakCount = 0
global frequencyInt

#CHANGES THE LABEL OF THE DAYS LEFT FRAME
def change_days(index):
  global days, frequencyInt
  #NEEDS TO ACCESS THE PILL OBJECTS FREQUENCY AND CHANGE IT TO AN INTEGER
  if evening_pills.Efrequency == "twice":
    frequencyInt = 2
  else:
    frequencyInt = 1
    
  total_pills_taken = evening_pills.Edosage * frequencyInt
  days = evening_pills.Equantity / total_pills_taken
  print("Number of days left: " + days)
  
  #setting the name to appropriate value 
  name = evening_pills[index].Ename

   

try:
        #!!!-----PUT IN A TIME.SLEEP() SOMEWHERE TO ACT AS A TIMER FOR HOW LONG IT TAKES TO SCAN A PRESCRIPTION------!!!
        count = 0
        show_page(count)
        '''
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
        '''
  
        count = 1
        show_page(count)
        '''
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
        # if button1_clicked == True:
        for i in range(len(evening_pills)):
            print(evening_pills[i].Econtainer + " dispensing")
            for j in range(evening_pills[i].Edosage):
                if button1_clicked == True:
                  count = 2
                  #GUI SWITCHES TO DISPENSING SCREEN
                  show_page(count)
                  button1_clicked = False
                print(str(evening_pills[i].Edosage) + " pills dispensing")
                print("calling pillOut")
                pillOut(i)
                count = 3
                #DISPLAYS THE DAYS LEFT FRAME (WITH PARAMETERS TO ACCESS DATA)
                change_days(i)
                show_page(count)
                print("Exit completed. Next pill is dispensing...")
            print("Next container is dispensing...")
            time.sleep(1)
        '''
        # button1_clicked == False (to reset)
        #INCREMENTING STREAKCOUNT BY ONE EACH TIME DISPENSING IS DONE || INCREMENT BEFORE DISPLAYING IT !!!!!
        streakCount += 1
        #show the streakframe
  
        #TESTING THE NAVIGATION BETWEEN FRAMES WITHOUT BUTTONS
        count = 2
        show_page(count)
        count = 3
        show_page(count)
        print("Finished Dispensing!") 
        count = 0
        show_page(count)
        #SWITCH BACK TO STREAK SCREEN
            
finally:
    GPIO.cleanup()

