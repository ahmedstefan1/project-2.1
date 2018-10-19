from tkinter import *
from linker import *


class Window:

    def openblinds(self):
        print("test1")

    def closeblinds(self):
        print("test2")

    def __init__(self, width=500, height=250):
        root = Tk()
        root.title("project 2.1")

        frame = Frame(root, width=width, height=height)
        frame.grid(column=0, row=0, columnspan=1000, rowspan=1000)

        com_port = StringVar(root)
        com_port_choices = [get_com_ports()]
        if com_port_choices[0] == "N/A":
            com_port.set("N/A")
        else:
            com_port.set("none chosen")
        print(len(com_port_choices))

        dropdownmenu = OptionMenu(root, com_port, *com_port_choices)
        dropdownmenu.grid(column=900, row=850)

        connect = Button(root, text="open connection", command=self.openblinds)
        connect.grid(column=900, row=900)

        button2 = Button(root, text="open blinds", command=self.closeblinds)
        button2.grid(column=900, row=100)
        button2 = Button(root, text="close blinds", command=self.closeblinds)
        button2.grid(column=900, row=200)

        root.iconbitmap('windowicon.ico')
        root.mainloop()


def main():
    w = Window()


if __name__ == '__main__':
    main()
