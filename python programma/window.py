from tkinter import *


class Window:
    def __init__(self, width=500, height=250):
        root = Tk()
        frame = Frame(root, width=width, height=height)
        frame.grid(column=0, row=0, columnspan=1000, rowspan=1000)

        button = Button(root, text="test").grid(column=1, row=1)

        root.mainloop()

