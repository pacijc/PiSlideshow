from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os

root = Tk(screenName="Slideshow Manager", baseName="Slideshow Manager", className="Slideshow Manager")
frm = ttk.Frame(root, padding=250)
frm.grid()

#Opens a file explorer dialog and checks that slected dir is valid
def browse_files():
    dirpath = filedialog.askdirectory(title = "Select a Folder")
    if dirpath:
        #update dir_path_label and valid path if the selected directory is valid
        if process_path(dirpath) != -1:dir_path_label.config(text=dirpath); show_send()
        else: hide_send()

#Checks that the contents of the folder are all jpg
def process_path(dirpath):
    try:
        if(len(os.listdir(dirpath)) == 0):raise Exception("The selected folder is empty")
        for filename in os.listdir(dirpath):
            if check_extension(filename) == -1: raise Exception("Please ensure all files in folder are .jpg")
    except Exception as e:
        dir_path_label.config(text=f"Error: {str(e)}")
        return -1

#check that the extension of a file is jpg
def check_extension(filename):
    extension = os.path.splitext(filename)[1]
    for test in (".jpg", ".jpeg", ".jfif", ".jpe", ".jif"):
        if test == extension: return 0
    return -1

#send folder of new slides to pi
def update_slides():
    print("Sent Slides")

def show_send():
    send_button.grid(column=0,row=0,columnspan=2)
def hide_send():
    send_button.grid_remove()
#---------------UI Elements------------------------#
#button which prompts for file selection
browse_button = ttk.Button(frm, text="Browse Files", command=browse_files)
browse_button.grid(column=0, row=1)

#displays path for selected folder
dir_path_label = ttk.Label(frm, text="")
dir_path_label.grid(column=1, row=1)

#only appears when process_path determines a path is valid
send_button = ttk.Button(frm, text="SEND", command=update_slides)

#quit button
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=2, columnspan=2)
root.mainloop()