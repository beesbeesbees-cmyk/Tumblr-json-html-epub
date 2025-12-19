import json
import os
import os.path
import shutil

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


class App(tk.Frame):
    def __init__(self, master): # Runs as soon as program starts
        super().__init__(master)
        
        frm = ttk.Frame(root, padding='0.1i')
        frm.grid()
        frm.rowconfigure(1, weight=3, minsize='0.5i')
        frm.rowconfigure(2, weight=3, minsize='0.5i')
        frm.columnconfigure(0, weight=3, minsize='0.5i')
        
        ttk.Button(
                frm, text="Where are your JSON files?", command=self.choose_json_directory).grid(column=0, row=0, columnspan=1, sticky="NW")
        self.jsonpath_display_text = tk.StringVar()
        self.jsonpath_display_text.set("Selected JSON Directory: ")
        self.jsonpath = ""
        self.json_directory_label = ttk.Label(frm, text="Selected JSON Directory: ", width=80)
        self.json_directory_label.grid(column=0, row=1, columnspan=3)
        self.json_directory_label['textvariable'] = self.jsonpath_display_text

        ttk.Button(
            frm, text="Where do you want your JSONs to go?", command=self.choose_end_directory).grid(column=1, row=0, columnspan=1)
        self.endpath_display_text = tk.StringVar()
        self.endpath_display_text.set("Selected end Directory: ")
        self.endpath = ""
        self.end_directory_label = ttk.Label(frm, text="Selected end Directory: ", width=80)
        self.end_directory_label.grid(column=0, row=2, columnspan=3)
        self.end_directory_label['textvariable'] = self.endpath_display_text
        
        self.status_display_text = tk.StringVar()
        self.status_label = ttk.Label(frm, text="", width=80)
        self.status_label.grid(column=0, row=3, columnspan=3)
        self.status_label['textvariable'] = self.status_display_text
        
        self.confirm_button = ttk.Button(frm, text="Confirm", command=self.execute) # Self passes itself as first param
        self.confirm_button.grid(column=1, row=4, columnspan=1, sticky="SE")
        self.confirm_button.state(['disabled'])
        self.exit_button = ttk.Button(frm, text="Exit", command=root.destroy)
        self.exit_button.grid(column=2, row=4, columnspan=1, sticky="SE")
        
        # directory_button.pack(pady=10)
        # self.choose_directory()
    
    def choose_json_directory(self):
        jsonpath = filedialog.askdirectory(title="Where are your JSON files?")
        self.jsonpath = jsonpath
        self.jsonpath_display_text.set(f"JSONs are in: {jsonpath}") # Sets text of label to htmlpath)
        if os.path.exists(jsonpath): # If path exists, enable button
            self.confirm_button.state(['!disabled'])

    def choose_end_directory(self):
        endpath = filedialog.askdirectory(title="Where are your HTML files?")
        self.endpath = endpath
        self.endpath_display_text.set(f"Selected Directory: {endpath}") # Sets text of label to htmlpath)
        if os.path.exists(endpath): # If path exists, enable button
            self.confirm_button.state(['!disabled'])
        
    def execute(self):
        jsonpath = self.jsonpath
        endpath = self.endpath

        for path, dirs, files in os.walk(jsonpath):
            print(f"{path}")
            for name in files:
                if name.endswith((".json")):
                    f = open(str(path + "\\" + name), encoding="utf-8-sig")
                    data = json.load(f)

                    if "date-gmt" in data.keys():
                        date = data['date-gmt']
                        year = date[:4]
                        month = date[6:7]
                        day = date[9:10]
                    elif "date" in data.keys() and "date-gmt" not in data.keys():
                        date = data['date']
                        year = date[:4]
                        month = date[6:7]
                        day = date[9:10]
                    else:
                        date = ''
                        year = "Unknown"
                        print(f"CANNOT DATE: {name}")

                    if os.path.exists(str(endpath + "\\" + year)) == False:
                        os.makedirs(str(endpath + "\\" + year))
                        print(f"A recieving folder has been created for {year}")

                    src_path = str(path + "\\" + name)
                    dest_path = str(endpath + "\\" + year + "\\" + name)
                    shutil.copy(src_path, dest_path)

root = tk.Tk()
root.title("JSON Organize by Year")
myapp = App(root)

myapp.mainloop()