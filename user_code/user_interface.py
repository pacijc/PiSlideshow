from tkinter import *
from tkinter import filedialog, messagebox, ttk
from pdf2image import convert_from_path
import os

DEFAULT_PAD = 10
WINDOW_COLOR = "#536878"
INSET_COLOR = "#36454f"

info_text = """
1. Click 'Browse Files' and select the PDF containing your slideshow
2. Once your file has been selected, press 'Convert' to prepare the slides
3. Click 'Quit' to exit program
4. Connect device to tv in order to start slideshow

To change slide duration, type duration in the box before pressing quit
"""

class FileWindow(Frame):
    #initialize sub window as a frame
    def __init__(self,parent):
        Frame.__init__(self, parent, bd=5, relief=RIDGE, bg=WINDOW_COLOR)
        self.parent = parent
        self.widgets()

    #add widgets to window
    def widgets(self):
        #displays path for selected folder
        self.dir_path_label = ttk.Label(self, text="\t\t\t\t\t", borderwidth=3, relief=SUNKEN, padding=3)
        self.dir_path_label.grid(column=1, row=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD)        

        #button which prompts for file selection
        self.browse_button = ttk.Button(self, text="Browse Files", command=lambda: browse_files(self.dir_path_label))
        self.browse_button.grid(column=0, row=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD)

class InfoWindow(Frame):
    #initialize sub window as a frame
    def __init__(self,parent):
        Frame.__init__(self, parent, bd=5, relief=RIDGE, bg=WINDOW_COLOR)
        self.parent = parent
        self.widgets()

    #add widgets to window
    def widgets(self):
        self.label = Label(self, text= "HOW TO USE", relief=GROOVE, bd=3, bg=WINDOW_COLOR, padx=3, pady=3)
        self.label.grid(row=0, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD)
        
        self.info = Label(self, text=info_text, bg=INSET_COLOR, justify=LEFT, relief=SUNKEN, borderwidth=5, padx=DEFAULT_PAD, pady=DEFAULT_PAD)
        self.info.grid(row=1, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD)

class TimeWindow(Frame):
    #initialize sub window as a frame
    def __init__(self,parent):
        Frame.__init__(self, parent, bd=5, relief=RIDGE, bg=WINDOW_COLOR)
        self.parent = parent
        self.time = StringVar()
        self.widgets()

    #add widgets to window
    def widgets(self):
        #slide label
        self.label = Label(self, text="Change Slide Duration", background=WINDOW_COLOR)
        self.label.grid(row=1, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="n")

        #slide duration entry box
        self.time = ttk.Entry(self,textvariable=self.time, justify=RIGHT, foreground="black")
        self.time.grid(row=1, column=1, padx=DEFAULT_PAD, pady=DEFAULT_PAD)
        
class ControlWindow(Frame):
    #initialize sub window as a frame
    def __init__(self,parent):
        Frame.__init__(self, parent, bd=5, relief=RIDGE, bg=WINDOW_COLOR)
        self.parent = parent
        self.widgets()

    #add widgets to window
    def widgets(self):
        #quit button
        self.quit = ttk.Button(self, text="Quit", command=lambda: quit(self))
        self.quit.grid(row=1, column=3, padx=DEFAULT_PAD, pady=DEFAULT_PAD)
        #convert button
        self.convert = ttk.Button(self, text="Convert", state=DISABLED, command=convert_pdf)
        self.convert.grid(row=1, column=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD)

class MainWindow(Tk):
    #init this window as root window
    def __init__(self):
        Tk.__init__(self)
        ttk.Style().theme_use('default')
        self.configure(background="#708090")
        self.mainWidgets()
        self.selectedFile = ""

    #add child windows to main window
    def mainWidgets(self):
        self.info_window = InfoWindow(self)
        self.info_window.grid(column=0, row=0, columnspan=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD)
        
        self.file_window = FileWindow(self)
        self.file_window.grid(column=0, row=1, columnspan=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD)

        self.control_window = ControlWindow(self)
        self.control_window.grid(column=1, row=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD)

        self.time_window = TimeWindow(self)
        self.time_window.grid(column=0, row=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD)
        

#-----------------Functions--------------------------------------

#Opens a file explorer dialog and checks that slected file is valid
def browse_files(label):
    pdf_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf")],
        title = "Select a Folder"
        )
    
    if not pdf_path:
       #disable_send()
        app.control_window.convert.config(state=DISABLED)

    else: 
        label.config(text=pdf_path)
        app.selectedFile=pdf_path
        #allow_send()
        app.control_window.convert.config(state=NORMAL)

#read contents from file
def get_text(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return content

#send folder of new slides to pi
#def update_slides():
#    cwd = os.getcwd()
#    path = cwd+"/active_slideshow"
#    print(path)
#    os.makedirs(path, exist_ok=True)
    
#convert pdf to png (potential issues with cross compatibility)
def convert_pdf():
    cwd = os.getcwd()
    output_folder = cwd+"/active_slideshow"
    try:
        os.rmdir(output_folder)
    except OSError as error:
        print(error)
    os.makedirs(output_folder, exist_ok=True)
    try:
        images = convert_from_path(app.selectedFile)
        for i, img in enumerate(images):
            img.save(os.path.join(output_folder, f"page_{i+1:03d}.png"), "PNG")

        messagebox.showinfo("Success", f"Saved {len(images)} pages to:\n{output_folder}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        
def update_duration():
    outputPath=os.getcwd()+"/Other/duration.txt"
    time = app.time_window.time.get()
    if(not time):
        return
    #check input is valid number
    try: 
        itime = int(time)
        if(itime not in range(1, 30)):
            messagebox.showerror("Error", "Please enter a number between 1 and 30")
            return -1
    except:
        messagebox.showerror("Error", "Please enter a number between 1 and 30")
        return -1
    
    # add proper string for duration to a file here
    durString = "feh -F --zoom max -D "+time+" --hide-pointer --sort name --version-sort"
    print(durString)
    with open(outputPath, "w") as file:
        file.write("#!/bin/bash\ncd \"$1\"\n"+durString)
        file.close()
    return
    #in pi, check if file updated, then change autostart script accordingly
    
    
def quit(self):
    if update_duration() == -1: return
    self.parent.destroy()
        
if __name__ == "__main__":
    app = MainWindow()
    app.title("PDF Slideshow App")
    app.mainloop()