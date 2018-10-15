from tkinter import *


class window:
    def __init__(self, width=500, height=250):
        root = Tk()
        frame = Frame(root, width=width, height=height)
        frame.grid()


        root.mainloop()

