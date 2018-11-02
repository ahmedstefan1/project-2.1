from tkinter import *
from python.linker import *
from python.performance_management import *
from math import *


class Window:
    com_port = None

    def openblinds(self):
        print("test1")

    def refresh_comports(self):
        print("refresh")

    # zorgt ervoor dat de verbinding word opgesteld
    def connect(self):
        global com_port
        choice = com_port.get()
        if choice is None or choice == "N/A" or choice == "none chosen":
            print("none selected")
        else:
            choice = choice[2:6]
            serial_connection(choice)
            try:
                serial_connection(choice)
            except:
                print("connection failed")

    def __init__(self, width=750, height=400, rows=100, columns=100):
        global com_port
        root = Tk()
        # geeft een titel aan de window
        root.title("project 2.1")
        # geeft de window de grootte die aangegeven is
        root.geometry((str(width)+"x" + str(height)))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        frame = Frame(root, width=width, height=height)
        frame.grid(column=0, row=0, rowspan=rows, columnspan=columns, sticky=(N, S, E, W))

        # maakt de com_port een stringvar in de root
        com_port = StringVar(root)
        # haalt alle compoorten op vanuit de functie get_com_ports in de linker.py en zet ze in een lijst
        com_port_choices = [get_com_ports()]
        # zet de default waarde voor de lijst
        com_port.set(com_port_choices[0])
        # maakt de dropdown menu waar je de compoorten kunt uitkiezen
        dropdownmenu = OptionMenu(frame, com_port, *com_port_choices)
        # plaats de dropdown menu in de grid
        dropdownmenu.grid(column=95, row=10)

        # maakt alle knoppen
        connect = Button(frame, text="open connection", command=lambda: background(self.connect))
        closeconn = Button(frame, text="close connection", command=close_connection)
        refresh = Button(frame, text="refresh, com_ports", command=self.refresh_comports)
        openblinds = Button(frame, text="open blinds", command=self.openblinds)
        closeblinds = Button(frame, text="close blinds", command=self.openblinds)

        # plaatst alle knoppen in de grid
        connect.grid(column=95, row=11)
        closeconn.grid(column=95, row=12)
        refresh.grid(column=95, row=9)
        openblinds.grid(column=95, row=80)
        closeblinds.grid(column=95, row=81)

        # maakt de canvassen
        canvas1 = Canvas(frame, width=ceil(width*0.1), height=ceil(height*0.2), bg='blue')
        canvas2 = Canvas(frame, width=ceil(width*0.1), height=ceil(height*0.2), bg='red')
        canvas3 = Canvas(frame, width=ceil(width*0.1), height=ceil(height*0.2), bg='green')

        # plaats de canvassen
        canvas1.grid(row=1, column=1, rowspan=ceil(rows * 0.8), columnspan=ceil(columns * 0.8))
        canvas2.grid(row=1, column=1, rowspan=ceil(rows * 0.8), columnspan=ceil(columns * 0.8))
        canvas3.grid(row=1, column=1, rowspan=ceil(rows*0.8), columnspan=ceil(columns*0.8))

        # zorgt voor het automatisch scalen van alle rows en colommen
        for i in range(columns):
            frame.columnconfigure(i, weight=1)
        for j in range(rows):
            frame.rowconfigure(j, weight=1)

        # zorgt voor mooi icoontje links bovenin
        root.iconbitmap('./python/windowicon.ico')

        root.mainloop()


def main():
    # maakt een object window
    w = Window()


if __name__ == '__main__':
    # runt de functie main direct na het uitvoeren van de code
    main()