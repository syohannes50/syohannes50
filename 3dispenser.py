import tkinter
import customtkinter as ctk

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
                      text = "You have {days} day(s) of {evening_pills[index].Ename} left", #days = variable 
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

#DEFINE GLOBAL DAYS VARIABLE
global days
global streakCount

global frequency = "twice"
global frequencyInt
#CHANGES FREQUENCY TO INTEGER
if frequency == "twice":
  frequencyInt = 2
else:
  frequencyInt = 1


def show_days(index):
  global days, frequencyInt
  if evening_pills.Efrequency == "twice":
  frequencyInt = 2
else:
  frequencyInt = 1
  if 2 == index:
    evening_pills.Edosage x frequencyInt
  else:
    page.pack_forget()  # Hide all other frames

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
        '''
        
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

