"""This module provides various functions to manipulate time values."""
import time
import PySimpleGUI as psg   # A framework to develop GUI application.

check_lists = []  # Declare a empty list.

"""Sets / Gets the current Theme. """
psg.theme("Purple")
current_time = time.strftime("%B %d,%Y %H:%M:%S %p")

label = psg.Text("Enter an item:")
label_time = psg.Text(current_time)

input_box = psg.InputText(tooltip="Type something...:", expand_x=True, key="-input-")   # Message that is shown here.
add_button = psg.Button("add")

list_box_text = psg.Text("Track of To-Dos:")
list_box = psg.Listbox(values=check_lists, size=(30, 10), expand_y=True, enable_events=True,
                       font=('Bold', 20), key="item")              # List of added items are shown here.

"""Button Element - Defines all possible buttons"""
edit_button = psg.Button("edit")
remove_button = psg.Button("remove")
clear_button = psg.Button("clear")

"""Create a window with all elements the title, layout for the window,specifies the font family, size, etc"""
window = psg.Window("Daily Routine",
                    layout=[[label_time], [label],
                            [[input_box, add_button]], [list_box_text], [list_box, edit_button, remove_button],
                            [clear_button]],
                    font=('Courier', 20)
                    )


while True:
    event, values = window.read()   # Call Windows read it returns event, values.
    """Add,Edit,Remove and Clear all the items in a box"""
    match event:
        case "add":
            get_item = values["-input-"]   # User enter the input here.
            check_lists.append(get_item)   # Append entered input with current list of items.
            window["item"].update(values=check_lists)  # Update the window.
            window["-input-"].update(value="")        # Update the input box.
        case "edit":
            try:
                item_to_edit = values["item"][0]  # Select an item from lists.
                update_item = psg.popup_get_text("Enter an updated item:")  # Pop-up box appears and enter the new item.
                if update_item:
                    """If new item added , replace old item with a new item"""
                    index = check_lists.index(item_to_edit)
                    check_lists[index] = update_item
                    window["item"].update(values=check_lists)
                else:
                    """If no new item added, keep old window """
                    window["-input-"].update(value="")

            except IndexError:
                psg.popup("Please Select at least one item from lists:")  # at-least one item to be selected to update
        case "remove":
            try:
                item_to_remove = values["item"][0]   # Select an item from lists.
                check_lists.remove(item_to_remove)   # Remove an item selected from lists
                window["item"].update(values=check_lists)
            except IndexError:
                psg.popup("Please Select at least one item to remove:")  # at-least one item to be selected to remove

        case "clear":
            check_lists.clear()   # Clears all lists available in a box
            window["item"].update(values=check_lists)   # Update a window

        case psg.WIN_CLOSED:
            break

"""Closes window.  Users can safely call even if window has been destroyed.   Should always call when done with
        a window so that resources are properly freed up within your thread."""
window.close()
