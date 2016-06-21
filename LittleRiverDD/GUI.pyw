import os
try:
    from Tkinter import *
except:
    from tkinter import *

from tkFileDialog import askdirectory, Open
import tkMessageBox
import thread
import time
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'llrd', 'thirdParty'))
import munch

class GUI(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title('Create Map from Geotagged Photos')

        self.lb = Listbox(self)

        # pack it all up
        self.pack(side=LEFT, fill=BOTH, expand=1, padx=10, pady=10)


def main():
    root = Tk()
    root.geometry("800x225")
    gui = GUI(root)
    root.mainloop()

if __name__ == '__main__':
main()