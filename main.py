import string
from tkinter import *
from tkinter import messagebox
import random

win = Tk()
win.title("Password Generator:")

def help_message():
    messagebox.showinfo('Help','The min value should be 15')

def created_password():
    entry_length = int(entry.get())
    if entry_length < 15:
        messagebox.showerror('ERROR','Password minimum length should be 15. Please re-try')
        return
    characters = string.ascii_letters+string.digits+string.punctuation
    password = "".join(random.choice(characters) for i in range(entry_length))
    password_entry.delete(0,END)
    password_entry.insert(0,password)


label = Label(text="Enter the length of the password:", height=5)
label.pack(side=TOP)

entry = Entry(win,width=20)
entry.pack(side=TOP, padx=10, pady=5)

generate_button = Button(win,text="Generate", command=created_password)
generate_button.pack(side=TOP,pady=10)

help_button= Button(win, text="Help", command=help_message)
help_button.pack(side=TOP, padx=10,pady=5)


label = Label(text="Password:", height=10)
label.pack(side=TOP)

password_entry = Entry(win, width=20)
password_entry.pack(side=TOP,padx=10, pady=10)

def clear():
    entry.delete(0, END)
    password_entry.delete(0, END)

clear_button = Button(win,text="Clear", command=clear)
clear_button.pack(side=TOP, pady=10)



win.mainloop()
