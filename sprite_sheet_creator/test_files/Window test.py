import getpass
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext


# Function to display the log file content in the rich text box
def display_log_file_content(event):
    item = tree.selection()[0]
    file_path = tree.item(item, "values")[0]

    with open(file_path, 'r') as file:
        log_content = file.read()
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, log_content)


# Get the current user
current_user = getpass.getuser()

# Create the main window
window = tk.Tk()
window.title("Log Viewer")

# Create the tree view
tree = ttk.Treeview(window)
tree.heading("#0", text="Applications")

# Add the root directories
maya_node = tree.insert("", tk.END, text="Maya")
nuke_node = tree.insert("", tk.END, text="Nuke")
houdini_node = tree.insert("", tk.END, text="Houdini")
substance_node = tree.insert("", tk.END, text="Substance Painter")

# Add the crash log file paths for each application
maya_log_path = f"C:\\Users\\{current_user}\\AppData\\Local\\Temp\\MayaCrash.log"
nuke_log_path = f"C:\\Users\\{current_user}\\AppData\\Local\\Temp\\NukeCrash.log"
houdini_log_path = f"C:\\Users\\{current_user}\\AppData\\Local\\Temp\\houdini_temp\\HoudiniCrash.log"
substance_log_path = f"C:\\Users\\{current_user}\\AppData\\Local\\Allegorithmic\\Substance Painter\\SubstanceCrash.log"

tree.insert(maya_node, tk.END, text="Maya Crash Log", values=(maya_log_path,))
tree.insert(nuke_node, tk.END, text="Nuke Crash Log", values=(nuke_log_path,))
tree.insert(houdini_node, tk.END, text="Houdini Crash Log", values=(houdini_log_path,))
tree.insert(substance_node, tk.END, text="Substance Painter Crash Log", values=(substance_log_path,))

tree.pack(side=tk.LEFT, fill=tk.Y)

# Create the rich text box
text_box = scrolledtext.ScrolledText(window)
text_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Bind the selection event to the display_log_file_content function
tree.bind("<<TreeviewSelect>>", display_log_file_content)

# Start the main event loop
window.mainloop()
