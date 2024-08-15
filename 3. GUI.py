import tkinter
from tkinter import *
import customtkinter as ctk
import time

#DEFINE GLOBAL VARIABLES FOR GUI
button1_clicked = False
name = ""
days = 0
streakCount = 0
frequencyInt = 0

#theme & color
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

#window size & title
window = ctk.CTk()
window.title('PillPal GUI')
window.geometry("800x480")


#----------------------------------------------------------STREAKFRAME (needs background)
streakframe = ctk.CTkFrame(window, 
                           width=800, 
                           height=480)
streakframe.pack(padx=5, pady=5)
streakframe.pack_propagate(False)

hi = ctk.CTkLabel(streakframe, 
                  width=800, 
                  height=80, 
                  text="Hi, PillPal User", 
                  fg_color='#ffff9c', 
                  text_color='black', 
                  font=('Sans-Serif', 30, 'bold'))
hi.pack(padx=10, pady=10)

streak = ctk.CTkLabel(streakframe, 
                      text="You're on a \n {streakCount} day streak!", 
                      font=('Sans-Serif', 40, 'bold'), 
                      fg_color='#ffb9d5')
streak.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
#------------------------------------------------------------READY FRAME 
readyframe = ctk.CTkFrame (window,
                           width = 800,
                           height = 480)
readyframe.pack(padx=5, pady=5)
readyframe.pack_propagate(False)
label1 = ctk.CTkLabel(readyframe,
                      width = 800,
                      height = 500,
                      text = "It's time to take your medication.",
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
label3 = ctk.CTkLabel(daysframe,
                      width = 800,
                      height = 500,
                      text = "You have {days} day(s) of {name} left", #days = v$
                      text_color = 'black',
                      font = ('Sans-Serif', 35, 'bold'),
                      fg_color = '#ffb9d5')
label3.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

hello = ctk.CTkLabel(daysframe,
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
def button():
    global button1_clicked
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



#CHANGES THE LABEL OF THE DAYS LEFT FRAME
def change_days(index):
  global days, frequencyInt
  #NEEDS TO ACCESS THE PILL OBJECTS FREQUENCY AND CHANGE IT TO AN INTEGER
  if evening_pills[index].Efrequency == "twice":
    frequencyInt = 2
  else:
    frequencyInt = 1
    
  total_pills_taken = evening_pills[index].Edosage * frequencyInt
  days = evening_pills.Equantity / total_pills_taken
  print("Number of days left: " + days)
  
  #setting the name to appropriate value 
  name = evening_pills[index].Ename


try:
        print("testing")
        '''
        #START WITH THE STREAK SCREEN
        count = 0
        show_page(count)
        
       
        #SHOW READY SCREEN
        count = 1
        show_page(count)
        

        #IF BUTTON IS CLICKED CALL FUNCTION TO MOVE ON TO DISPENSING (SCREEN)
        
        if button_clicked == True:
                #CHECK AGAIN 
                if button1_clicked == True:
                  #GUI STAYS ON DISPENSING SCREEN
                  count = 2
                  show_page(count)
                  #RESET BUTTON
                  button1_clicked = False
                  print("Pills are dispensing....")
                  #DISPLAYS THE DAYS LEFT FRAME (WITH PARAMETERS TO ACCESS DATA)
                  count = 3
                  #Remember to update the quantity (evening_pills[index].Equantity -= evening_pills[index].dosage)
                  change_days(i)
                  show_page(count)
                  print("Exit completed. Next pill is dispensing...")
            print("Next container is dispensing...")
            time.sleep(3)
      
        button1_clicked == False 
        #INCREMENTING STREAK COUNT BY ONE EACH TIME DISPENSING IS DONE BEFORE DISPLAYING STREAK SCREEN
        streakCount += 1
        #SHOW THE STREAK SCREEN AGAIN
        count = 0
        show_page(count)
        '''
        '''
        #TESTING THE NAVIGATION BETWEEN FRAMES WITHOUT BUTTONS
        #START WITH THE STREAK SCREEN
        count = 0
        show_page(count)
        time.sleep(3)
        #SHOW READY SCREEN
        count = 1
        show_page(count)
        time.sleep(3)
        #SHOW DISPENSING SCREEN
        count = 2
        show_page(count)
        time.sleep(3)
        #SHOW ALERT SCREEN
        count = 3
        show_page(count)
        print("Finished Dispensing!") 
        time.sleep(3)
        #GO BACK TO STREAK SCREEN
        count = 0
        show_page(count)
        '''
            
finally:
    GPIO.cleanup()

