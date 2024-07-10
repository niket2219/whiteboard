from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os

root = Tk()
root.title("White Board")
root.geometry("1050x570+150+50")
root.configure(bg="#f2f3f5")
root.resizable(False, False)

current_x = 0
current_y = 0
color = "black"
tool = "pencil"  # Variable to track the current tool


# Lists to store drawing actions for undo/redo
drawing_actions = []
redo_actions = []


def locate_xy(event):
    global current_y, current_x
    current_x = event.x
    current_y = event.y


def addline(event):
    global current_x, current_y
    if tool == "pencil":
        line = canvas.create_line((current_x, current_y, event.x, event.y),
                                  width=get_current_value(), fill=color, capstyle=tk.ROUND, smooth=True)
        drawing_actions.append(line)
        current_x, current_y = event.x, event.y


def show_color(new_color):
    global color
    global tool
    color = new_color
    tool = "pencil"  # Set the tool to pencil when a color is selected
    canvas.bind('<B1-Motion>', addline)


def erase(event):
    global eraser_highlight_rect
    if tool == "eraser":
        size_value = int(currentValue.get())
        x1, y1 = (event.x - size_value), (event.y - size_value)
        x2, y2 = (event.x + size_value), (event.y + size_value)
        erase_rect = canvas.create_rectangle(
            x1, y1, x2, y2, fill='red', outline='white')
        drawing_actions.append(erase_rect)


def selecteraser():
    global tool
    tool = "eraser"  # Set the tool to eraser when the eraser button is selected
    canvas.bind('<B1-Motion>', erase)


def insertimage():
    global filename
    global f_img
    global my_img
    global original_image

    filename = askopenfilename(initialdir=os.getcwd(), title="Select image file", filetypes=(
        ("JPG File", "*.jpg"), ("All Files", "*.*")))
    original_image = Image.open(filename)

    f_img = ImageTk.PhotoImage(original_image)
    my_img = canvas.create_image(180, 50, image=f_img)
    drawing_actions.append(my_img)
    canvas.bind("<B3-Motion>", my_callback)
    canvas.bind("<B2-Motion>", resize_image)


def my_callback(event):
    global f_img
    canvas.coords(my_img, event.x, event.y)


def resize_image(event):
    global f_img
    global my_img
    global original_image

    new_width = event.x
    new_height = event.y

    resized_image = original_image.resize(
        (new_width, new_height), Image.LANCZOS)
    f_img = ImageTk.PhotoImage(resized_image)

    canvas.itemconfig(my_img, image=f_img)


def undo_action():
    if drawing_actions:
        last_action = drawing_actions.pop()
        canvas.delete(last_action)
        redo_actions.append(last_action)


def redo_action():
    if redo_actions:
        last_action = redo_actions.pop()
        if isinstance(last_action, int):  # If it's a line or rectangle
            drawing_actions.append(canvas.coords(last_action))
        elif isinstance(last_action, tk.PhotoImage):  # If it's an image
            my_img = canvas.create_image(180, 50, image=last_action)
            drawing_actions.append(my_img)


# Sidebar
color_box = ImageTk.PhotoImage(file="color_pallete.png")
Label(root, image=color_box, bg="#f2f3f5").place(x=10, y=20)

eraser = PhotoImage(file="erase.png")
Button(root, image=eraser, bg="#f2f3f5",
       command=selecteraser).place(x=26, y=380)

importimage = PhotoImage(file="erase.png")
Button(root, image=importimage, bg="#f2f3f5",
       command=insertimage).place(x=26, y=430)

# Color palette
colors = Canvas(root, bg="#fff", width=40, height=320, bd=0)
colors.place(x=26, y=43)


def display_palette():
    id = colors.create_rectangle((6, 6, 37, 35), fill="black")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('black'))

    id = colors.create_rectangle((6, 41, 37, 70), fill="grey")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('grey'))

    id = colors.create_rectangle((6, 76, 37, 105), fill="brown")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('brown'))

    id = colors.create_rectangle((6, 111, 37, 140), fill="green")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('green'))

    id = colors.create_rectangle((6, 146, 37, 175), fill="blue")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('blue'))

    id = colors.create_rectangle((6, 181, 37, 210), fill="pink")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('pink'))

    id = colors.create_rectangle((6, 216, 37, 245), fill="orange")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('orange'))

    id = colors.create_rectangle((6, 251, 37, 280), fill="yellow")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('yellow'))

    id = colors.create_rectangle((6, 286, 37, 315), fill="red")
    colors.tag_bind(id, '<Button-1>', lambda x: show_color('red'))


display_palette()

# Main screen
canvas = Canvas(root, width=930, height=500,
                background="white", cursor="hand2")
canvas.place(x=100, y=10)

canvas.bind('<Button-1>', locate_xy)

# Slider
currentValue = tk.DoubleVar()


def get_current_value():
    return '{: .2f}'.format(currentValue.get())


def slider_changed(event):
    value_label.configure(text=get_current_value())


slider = Scale(root, from_=0, to=100, orient="horizontal",
               command=slider_changed, variable=currentValue)
slider.place(x=7, y=517)

value_label = Label(root, text=get_current_value())
value_label.place(x=120, y=535)

# Undo/Redo buttons
undo_button = Button(root, text="Undo", command=undo_action)
undo_button.place(x=10, y=10)

redo_button = Button(root, text="Redo", command=redo_action)
redo_button.place(x=50, y=10)

root.mainloop()
