from tkinter import *
from tkinter import filedialog, messagebox, ttk
from pdf2image import convert_from_path
import subprocess
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
        self.label.grid(row=0, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="n")

        #displays path for selected folder
        self.dir_path_label = ttk.Label(self, text="")
        self.dir_path_label.grid(column=0, row=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD)        

        #button which prompts for file selection
        self.browse_button = ttk.Button(self, text="Browse Files", command=lambda: browse_files(self.dir_path_label))
        self.browse_button.grid(column=0, row=1, padx=DEFAULT_PAD, pady=DEFAULT_PAD)

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

        self.label = Label(self, text="Use this slider to change the duration of each slide")
        self.label.grid(row=1, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="n")

        self.time = ttk.Spinbox(self, from_=1, to=30)
        self.time.grid(row=2, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD)

class ControlWindow(Frame):
    #initialize sub window as a frame
    def __init__(self,parent):
        Frame.__init__(self, parent, bg="red")
        self.parent = parent
        self.widgets()

    #add widgets to window
    def widgets(self):
        self.label = Label(self, text="Control window")
        self.label.grid(row=0, column=0, columnspan=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD)

        #send files to the pi
        #only appears when process_path determines a path is valid
        self.send_button = ttk.Button(self, text="SEND", state=DISABLED, command=update_slides)
        self.send_button.grid(row=1, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="w")
        #quit button
        self.quit = ttk.Button(self, text="Quit", command=self.parent.destroy)
        self.quit.grid(row=1, column=1, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="e")
        #convert button
        self.convert = ttk.Button(self, text="Convert", command=convert_pdf)
        self.convert.grid(row=2, column=0,columnspan=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD)

class MainWindow(Tk):
    #init this window as root window
    def __init__(self):
        Tk.__init__(self)
        self.mainWidgets()
        self.selectedFile = ""

    #add child windows to main window
    def mainWidgets(self):
        self.file_window = FileWindow(self)
        self.file_window.grid(column=0, row=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="w")

        self.settings_window = SettingsWindow(self)
        self.settings_window.grid(column=0, row=1, columnspan=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="w")

        self.control_window = ControlWindow(self)
        self.control_window.grid(column=1, row=1, columnspan=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="e")

        self.info_window = InfoWindow(self)
        self.info_window.grid(column=1, row=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky="w")

#-----------------Functions--------------------------------------

#Opens a file explorer dialog and checks that slected file is valid
def browse_files(label):
    pdf_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf")],
        title = "Select a Folder"
        )
    
    if not pdf_path: disable_send()
    else: 
        label.config(text=pdf_path)
        app.selectedFile=pdf_path
        allow_send()
        #update dir_path_label and show send button if the selected directory is valid
        #if process_path(pdf_path, label) != -1:label.config(text=pdf_path); allow_send()
        #else: disable_send()

#control activeness of send button
def allow_send():
    app.control_window.send_button.config(state=NORMAL)

def disable_send():
    app.control_window.send_button.config(state=DISABLED)

#read contents from file
def get_text(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return content

#send folder of new slides to pi
def update_slides():
    success = subprocess.run(["bash", "./user_code/set_active.sh", app.file_window.dir_path_label.cget("text")])
    if success: print("Sent Slides from this filepath:" + app.file_window.dir_path_label.cget("text"))

#convert pdf to png (potential issues with cross compatibility)
def convert_pdf():
    output_folder = os.path.splitext(app.selectedFile)[0] + "_slides"
    os.makedirs(output_folder, exist_ok=True)
    try:
        images = convert_from_path(app.selectedFile)
        for i, img in enumerate(images):
            img.save(os.path.join(output_folder, f"page_{i+1:03d}.png"), "PNG")

        messagebox.showinfo("Success", f"Saved {len(images)} pages to:\n{output_folder}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()