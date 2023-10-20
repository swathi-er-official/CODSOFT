"""Tkinter provides classes which allow the display, positioning and
control of widgets"""
from tkinter import *
import math  #This module provides access to the mathematical functions

"""Create a tkinter window"""
win = Tk()
win.title("Calculator")

expression = ""

"""Value holder for strings variables."""
input_text = StringVar()

"""Frame widget for which may contain other widgets."""
frame = Frame(win, width=250, height=50, bd=10, highlightcolor="red", highlightthickness=3)

frame.pack(side=TOP)

"""Entry widget which allows displaying simple text."""
input_field = Entry(frame, font=("arial", 18, "bold"), textvariable=input_text,
                    width=20, bg="yellow", bd=10, justify=RIGHT)

input_field.pack(ipady=10)

"""button box widget"""
calc_box = Frame(win, width=350, height=250, bg="purple")
calc_box.pack()

error = Label(frame,text="")
error.pack()


"""Function to show the item called in input_field"""
def bt_click(item):
    global expression
    expression = expression + str(item)
    input_text.set(expression)



"""Function to show the percentage value """
def bt_percent():
    global expression
    try:
        expression = float(input_field.get())  # get the number  and convert to float from str
        output = expression / 100             # Divide the value by 100
        input_text.set(output)
        expression = str(output)
    except:
        error.config(text="ERROR")  #show ERROR if pressed percentage button before entering the number


"""Function to show the square root of the value"""
def bt_sqt():
    global expression
    try:
        expression = float(input_field.get())
        output = math.sqrt(expression)  # method to return the square root of a number
        input_text.set(output)
        expression = str(output) #set number to str
    except:
        error.config(text="ERROR")  #show ERROR if pressed square root button before entering the number


"""Function to clear all the items """
def bt_clear():
    global expression
    expression = ""
    input_text.set("")
    error.config(text="")  # Press AC button to clear the ERROR label

"""Equal function"""
def bt_equal():
    global expression
    result = str(eval(expression))
    input_text.set(result)
    expression = result

"""Function to clear the item entered one by one from right side"""
def bt_remove():
    global expression
    input_field.delete(len(input_field.get())-1)
    final = input_field.get()
    expression = final

Box = ["<*","\u221a","%","/","7","8","9","*","4","5","6","-","1","2","3","+","AC","0",".","="]

"""enumerate is useful for obtaining an indexed list Box."""
for i ,label in enumerate(Box):
        if label == "AC":
            button = Button(calc_box, text=label,fg="black",width=10, height=2, bd=0, bg="grey80",command=lambda:bt_clear())
        elif label == "<*":
            button = Button(calc_box, text=label, fg="black",width=10, height=2, bd=0, bg="grey80", command=lambda: bt_remove())
        elif label == "%":
                button = Button(calc_box, text=label, fg="black",width=10, height=2, bd=0, bg="grey80", command=lambda: bt_percent())
        elif label =="\u221a":
            button = Button(calc_box, text=label, fg="black", width=10, height=2, bd=0, bg="grey80",command=lambda: bt_sqt())
        elif label == "=":
            button = Button(calc_box, text=label, fg="black", width=10, height=2, bd=0, bg="grey80",command=lambda: bt_equal())
        else:
            button = Button(calc_box, text=label, fg="black",width=10, height=2, bd=0, bg="grey80",
                            command=lambda arg=label: bt_click(arg))

        button.grid(row=i // 4, column=i % 4, padx=3, pady=3)

"""Call the mainloop of Tkinter."""
win.mainloop()