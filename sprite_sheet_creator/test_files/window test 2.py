import tkinter as tk

def show_message():
    message_label.config(text="Hello, Tkinter!")

# Create the main window
window = tk.Tk()
window.title("Tkinter Example")
window.geometry("300x150")  # Set the window size

# Create a label to display the message
message_label = tk.Label(window, text="Click the button to see a message.", font=("Arial", 16))
message_label.pack(pady=20)

# Create a button
button = tk.Button(window, text="Click me!", command=show_message)
button.pack()

# Start the main event loop
window.mainloop()
