from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os

DEFAULT_PAD = 10

class FileWindow(Frame):
    #initialize sub window as a frame
    def __init__(self,parent):
        Frame.__init__(self, parent, bg="green")
        self.parent = parent
        self.widgets()

    #add widgets to window
    def widgets(self):
        self.label = Label(self, text="File window")
        self.label.grid(row=0, column=0, padx=100, sticky="n")

        #displays path for selected folder
        self.dir_path_label = ttk.Label(self, text="")
        self.dir_path_label.grid(column=0, row=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD)        

        #button which prompts for file selection
        self.browse_button = ttk.Button(self, text="Browse Files", command=lambda: browse_files(self.dir_path_label))
        self.browse_button.grid(column=0, row=1, padx=50, pady=50)

class InfoWindow(Frame):
    #initialize sub window as a frame
    def __init__(self,parent):
        Frame.__init__(self, parent, bg="purple")
        self.parent = parent
        self.widgets()

    #add widgets to window
    def widgets(self):
        self.label = Label(self, text="Info window")
        self.label.grid(row=0, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="n")

        self.info = ttk.Label(self, text=get_text('user_code/info.txt'))
        self.info.grid(row=0, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD)

class SettingsWindow(Frame):
    #initialize sub window as a frame
    def __init__(self,parent):
        Frame.__init__(self, parent, bg="blue")
        #self.grid_propagate(False)
        self.parent = parent
        self.widgets()

    #add widgets to window
    def widgets(self):
        self.label = Label(self, text="Settings window")
        self.label.grid(row=0, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="n")

class ControlWindow(Frame):
    #initialize sub window as a frame
    def __init__(self,parent):
        Frame.__init__(self, parent, bg="red")
        self.parent = parent
        self.widgets()

    #add widgets to window
    def widgets(self):
        self.label = Label(self, text="Control window")
        self.label.grid(row=0, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD)

        #send files to the pi
        #only appears when process_path determines a path is valid
        self.send_button = ttk.Button(self, text="SEND", state=DISABLED, command=update_slides)
        self.send_button.grid(row=1, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="w")
        #quit button
        self.quit = ttk.Button(self, text="Quit", command=self.parent.destroy)
        self.quit.grid(row=1, column=1, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="e")

class MainWindow(Tk):
    #init this window as root window
    def __init__(self):
        Tk.__init__(self)
        self.mainWidgets()

    #add child windows to main window
    def mainWidgets(self):
        self.file_window = FileWindow(self)
        self.file_window.grid(column=0, row=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="w")

        self.settings_window = SettingsWindow(self)
        self.settings_window.grid(column=0, row=1, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="w")

        self.control_window = ControlWindow(self)
        self.control_window.grid(column=3, row=1, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="e")

        self.info_window = InfoWindow(self)
        self.info_window.grid(column=3, row=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="e")

#-----------------Functions--------------------------------------

#Opens a file explorer dialog and checks that slected dir is valid
def browse_files(label):
    dirpath = filedialog.askdirectory(title = "Select a Folder")
    if dirpath:
        #update dir_path_label and show send button if the selected directory is valid
        if process_path(dirpath, label) != -1:label.config(text=dirpath); show_send()
        else: hide_send()

#Checks that the contents of the folder are all jpg
def process_path(dirpath, label):
    try:
        if(len(os.listdir(dirpath)) == 0):raise Exception("The selected folder is empty")
        for filename in os.listdir(dirpath):
            if check_extension(filename) == -1: raise Exception("Please ensure all files in folder are .jpg")
    except Exception as e:
        label.config(text=f"Error: {str(e)}")
        return -1

#check that the extension of a file is jpg
def check_extension(filename):
    extension = os.path.splitext(filename)[1]
    for test in (".jpg", ".jpeg", ".jfif", ".jpe", ".jif"):
        if test == extension: return 0
    return -1

#control visibility of send button
def show_send():
    app.control_window.send_button.config(state=NORMAL)
def hide_send():
    app.control_window.send_button.config(state=DISABLED)

def get_text(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return content

#send folder of new slides to pi
def update_slides():
    
    print("Sent Slides")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()