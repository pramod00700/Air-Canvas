import tkinter as tk

def avoid():
    pass
# Create a Tkinter window
def notification():
    root = tk.Tk()

    # Set the window size and position
    root.geometry("200x100+400+300")

    # Create a label with the message
    label = tk.Label(root, text="image Saved successfully",font=21)
    label.pack(pady=20)

    # Define a function to close the window after 3 seconds
    def close_window():
        root.after(1000, root.destroy)

    # Call the close_window() function to close the window after 3 seconds
    close_window()

    # Start the Tkinter event loop
    root.mainloop()

