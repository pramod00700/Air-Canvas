import tkinter as tk
# from tkinter import filedialog
from ppt import draw_on_file as dof
from painter_test import paint
# Create the main window
root = tk.Tk()
root.title("Air Canvas")

# Load the image
# file_path = "C:/Users/Pramod/Downloads/img.jpeg"
image = tk.PhotoImage(file="img1.png")

# Create an image widget to hold the image
image_label = tk.Label(root, image=image)
image_label.pack()

# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack()

# Create a "New" button
def new_file():
    paint()

new_button = tk.Button(button_frame, text="New", font=("Arial", 16), command=new_file)
new_button.pack(side="left", padx=10)

# Create an "Open" button
def open_file():
    dof()

    


open_button = tk.Button(button_frame, text="Open", font=("Arial", 16), command=open_file)
open_button.pack(side="left", padx=10)

# Create an "About us" button``
def about_us():
    # Create a new window
    about_window = tk.Toplevel(root)
    about_window.title("About us")
    
    # Add the image to the window
    image_label = tk.Label(about_window, image=image)
    image_label.pack(side="left", padx=20, pady=20)
    
    # Add the text to the window
    text = "This is my application. It does stuff and things."
    text_label = tk.Label(about_window, text=text, font=("Arial", 16))
    text_label.pack(side="left", padx=20, pady=20)

about_button = tk.Button(button_frame, text="About us", font=("Arial", 16), command=about_us)
about_button.pack(side="left", padx=10)

# Run the main event loop
root.mainloop()