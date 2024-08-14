import tkinter
import customtkinter as ctk

#theme & color
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

#window size & title
window = ctk.CTk()
window.title('PillPal GUI')
window.geometry("800x480")

#-------------------------------------------------STREAKFRAME
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

hi = ctk.CTkLabel(streakframe,
                  width = 800,
                  height = 80,
                  text = "Hi, PillPal User",
                  fg_color = '#ffff9c',
                  text_color = 'black',
                  font = ('Sans-Serif', 30, 'bold'))
hi.pack(padx=10, pady=10)


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



#-------------------------------------------------------DISPENSE FRAME 

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



#---------------------------------------------DAYS LEFT FRAME STUFF

daysframe = ctk.CTkFrame (window,
                           width = 800,
                           height = 480)
daysframe.pack(padx=5, pady=5)
daysframe.pack_propagate(False)
label3 = ctk.CTkLabel(readyframe,
                      width = 800,
                      height = 500,
                      text = "You have 10 day(s) of Cymbalta left",
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
