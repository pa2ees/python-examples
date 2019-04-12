from Tkinter import *
from tkFileDialog import *
import tkFileDialog
from subprocess import call

import test1
test1 = reload(test1)


def openDir():
    if entry.get() == '':
        initial_dir = "F:/Capture Data"
    else:
        initial_dir = entry.get()
    entry_dir = tkFileDialog.askdirectory(parent=root, initialdir=initial_dir)
    if entry_dir != '':
        entry_val.set(entry_dir)

def startAnalysis():
    call("C:/Altera/11.0/quartus/bin/quartus_stp -t \"D:/Google Drive/pythonscripts/tmp/testscript.tcl\"")
    test1.analyze_folder(entry.get(), 0)
	#root.update()
    #print(overwrite)
	
root = Tk()

entry_val = StringVar()
entry_val.set("C:/temp/")

overwrite = IntVar()
overwrite.set(1)

legendon = IntVar()
legendon.set(1)

root.title("Doofus")

label = Label(root, text="Directory:")
label.grid(row = 0)
entry = Entry(root, width = 50, textvariable = entry_val)
entry.grid(row = 0, column = 1, padx = 5, pady = 2)
button = Button(root, text = "Open", command = openDir, padx = 5)
button.grid(row = 0, column = 2, padx = 5, pady = 2)
overwrite_checkbox = Checkbutton(root, text = "Overwrite", variable = overwrite, onvalue=1, offvalue=0)
overwrite_checkbox.grid(row = 1, column = 0, padx = 5, pady = 2)
Label(root, text = "Legend: ").grid(row = 2, column = 0, padx = 5, pady = 2)
Radiobutton(root, text = "On", value = 1, variable = legendon).grid(row = 2, column = 1, padx = 5, pady = 2)
Radiobutton(root, text = "Off", value = 1, variable = legendon).grid(row = 2, column = 2, padx = 5, pady = 2)
Button(root, text = "Start", command = startAnalysis).grid(row = 8, column = 0, padx = 5, pady = 2)

root.mainloop()
