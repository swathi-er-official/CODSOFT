"""A collection of string constants"""
import string
from tkinter import *           #Tkinter provides classes which allow the display, positioning and control of widgets
from tkinter import messagebox  #This module provides an interface to the native message boxes
import random                   #Random variable generators

win = Tk()
win.title("Password Generator:")

"""Configure resources of a widget"""
win.configure(bg="gold")


label = Label(text="Username:",font="Arial",fg="blue", bg="gold")
label.grid(row=0, column=0)

name_entry = Entry(win, width=20)
name_entry.grid(row=0, column=1)

label = Label(text="Enter the length of the password:",font="Arial",fg="blue", bg="gold")
label.grid(row=1, column=0)

entry = Entry(win, width=20)
entry.grid(row=1, column=1)


def help_message():
    messagebox.showinfo('Help','The minimum value should be 15')  # Help Button message


help_button= Button(win, text="Help",command=help_message, fg="teal", bg="silver")
help_button.grid(row=1, column=2)


"""Function to generate password"""
def created_password():
    entry_length = entry.get()# user input
    if not entry_length.isnumeric():
        messagebox.showerror('ERROR','Only numbers are allowed')
        return
    elif int(entry_length) < 15:
        messagebox.showerror('ERROR','Password minimum length should be 15. Please re-try')
        return
    characters = string.ascii_letters+string.digits+string.punctuation
    password = "".join(random.choice(characters) for i in range(int(entry_length)))  #Concatenate any number of strings
    password_entry.delete(0,END)    #Delete text from FIRST to LAST (not included).
    password_entry.insert(0,password)  #Insert STRING at INDEX.

"""Function to generate message"""
def generate_message():
    if entry.get() == "":
        messagebox.showerror("ERROR", "Please enter the length of the password")
        return
    elif name_entry.get() == "":
        messagebox.showerror("ERROR", "Please enter the username")
        return
    created_password()


generate_button = Button(win, text="Generate", command=generate_message,font="Arial", fg="dark violet", bg="lavender")
generate_button.grid(row=2, column=1)


label = Label(text="Password:", height=5, font="Arial",fg="blue", bg="gold")
label.grid(row=3, column=0)

password_entry = Entry(win, width=30)
password_entry.grid(row=3, column=1)


"""Function to clear the entries"""
def reset():
    entry.delete(0, END)
    password_entry.delete(0, END)
    name_entry.delete(0, END)


reset_button = Button(win,text="Reset", font="bold", command=reset, fg="red", bg="silver")
reset_button.grid(row=4, column=2)

"""Call the mainloop of Tk."""
win.mainloop()