import tkinter
import customtkinter as ctk

# Theme & color
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

# Create the main window
window = ctk.CTk()
window.title('PillPal GUI')
window.geometry("800x480")

# Function to show the Streak1 screen
def show_streak1():
    clear_window()
    
    streak = ctk.CTkLabel(self,
                          text = "You're on a \n [] day streak!",
                          font = ('Sans-Serif', 40, 'bold'),
                          fg_color = '#ffb9d5')
    streak.pack()
    button2 = ctk.CTkButton(
        window,
        text="next",
        text_color='black',
        font=('Sans-Serif', 20, 'bold'),
        width=300,
        height=75,
        fg_color='#ff78ae',
        border_width=5,
        border_color='red',
        hover_color='red',
        command=show_ready2
    )
    button2.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

    hi = ctk.CTkLabel(
        window,
        width=800,
        height=80,
        text="Hi, PillPal User",
        fg_color='#ffff9c',
        text_color='black',
        font=('Sans-Serif', 30, 'bold')
    )
    hi.place(relx=0.5, rely=0.075, anchor=tkinter.CENTER)

# Function to show the Ready2 screen
def show_ready2():
    clear_window()

    label1 = ctk.CTkLabel(
        window,
        width=800,
        height=480,
        text="It's time to take your medication",
        text_color='black',
        font=('Sans-Serif', 35, 'bold'),
        fg_color='#ffb9d5'
    )
    label1.pack()

    button1 = ctk.CTkButton(
        window,
        text="Dispense Now",
        text_color='black',
        font=('Sans-Serif', 20, 'bold'),
        width=300,
        height=75,
        fg_color='#ff78ae',
        border_width=5,
        border_color='red',
        hover_color='red',
        command=show_dispense3
    )
    button1.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

# Function to show the Dispense3 screen
def show_dispense3():
    clear_window()

    label2 = ctk.CTkLabel(
        window,
        width=800,
        height=500,
        text="Dispensing...",
        text_color='black',
        font=('Sans-Serif', 40, 'bold'),
        fg_color='#ffb9d5'
    )
    label2.pack()

    testbutton = ctk.CTkButton(window, text="test", command=show_daysleft4)
    testbutton.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)

# Function to show the Daysleft4 screen
def show_daysleft4():
    clear_window()

    label3 = ctk.CTkLabel(self,
                      width = 800,
                      height = 500,
                      text = "You have {days} day(s) of {evening_pills[index].Ename} left", #days = variable
                      text_color = 'black',
                      font = ('Sans-Serif', 35, 'bold'),
                      fg_color = '#ffb9d5')
    label3.pack()
    hello = ctk.CTkLabel(
        window,
        width=800,
        height=80,
        text="Hi, PillPal User",
        fg_color='#ffff9c',
        text_color='black',
        font=('Sans-Serif', 30, 'bold')
    )
    hello.place(relx=0.5, rely=0.075, anchor=tkinter.CENTER)

    testbutton1 = ctk.CTkButton(window, text="Back to Streak", command=show_streak1)
    testbutton1.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

# Helper function to clear the window
def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

# Start by showing the first screen
show_streak1()

# Start the main event loop
window.mainloop()
