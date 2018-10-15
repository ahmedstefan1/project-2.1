from tkinter import *
from linker import *

class Window:

    def openblinds(self):
        print("test1")
    def closeblinds(self):
        print("test2")

    def __init__(self, width=500, height=250):
        root = Tk()
        frame = Frame(root, width=width, height=height)
        frame.grid(column=0, row=0, columnspan=1000, rowspan=1000)

        button1 = Button(root, text="open blinds", command=self.openblinds)
        button1.grid(column=900, row=900)
        button2 = Button(root, text="close blinds", command=self.closeblinds)
        button2.grid(column=900, row=850)

        root.mainloop()

def main():
    w = Window()


if __name__ == '__main__':
    main()