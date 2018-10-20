from tkinter import *
from linker import *


class Window:
    com_port = None

    def openblinds(self):
        print("test1")

    def closeblinds(self):
        print("test2")

    def refresh_comports(self):
        print("refresh")

    def connect(self):
        global com_port
        choice = com_port.get()

        print(choice)
        if choice is None or choice == "N/A" or choice == "none chosen":
            print("none selected")
        else:
            choice = choice[2:6]
            try:
                serial_connection(choice)
            except:
                print("connection failed")

    def __init__(self, width=500, height=250, rows=10, columns=10):
        global com_port
        root = Tk()
        root.title("project 2.1")
        root.geometry((str(width)+"x" + str(height)))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        amount_rows = rows
        amount_col = columns
        frame = Frame(root, width=width, height=height)
        frame.grid(column=0, row=0, rowspan=amount_rows, columnspan=amount_col, sticky=(N, S, E, W))

        com_port = StringVar(root)
        com_port_choices = [get_com_ports()]
        if com_port_choices[0] == "N/A":
            com_port.set("N/A")
        else:
            com_port.set("none chosen")
            dropdownmenu = OptionMenu(frame, com_port, *com_port_choices)
            dropdownmenu.grid(column=(amount_col-1), row=(amount_rows-1))

            connect = Button(frame, text="open connection", command=self.connect)
            connect.grid(column=(amount_col-1), row=(amount_rows-2))

        button3 = Button(frame, text="refresh, com_ports", command=self.refresh_comports)
        button3.grid(column=(amount_col-1), row=(amount_rows-3))

        button2 = Button(frame, text="open blinds", command=self.closeblinds)
        button2.grid(column=(amount_col-10), row=(amount_rows-8))

        button2 = Button(frame, text="close blinds", command=self.closeblinds)
        button2.grid(column=(amount_col-10), row=(amount_rows-9))

        for i in range(amount_col):
            frame.columnconfigure(i, weight=1)
        for j in range(amount_rows):
            frame.rowconfigure(j, weight=1)

        root.iconbitmap('windowicon.ico')
        root.mainloop()


def main():
    w = Window()


if __name__ == '__main__':
    main()
