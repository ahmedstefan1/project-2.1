from tkinter import *
from python.linker import *
from python.performance_management import *
from math import *


class Window:
    com_port = None
    connection_label = Label

    def openblinds(self):
        print("test1")

    # zorgt ervoor dat de verbinding word opgesteld
    def connect(self):
        global com_port, connection_label
        choice = com_port.get()
        if choice is None or choice == "N/A" or choice == "none chosen":
            print("none selected")
        else:
            choice = choice[2:6]
            try:
                connection_label.config(text="connection: connected")
                serial_connection(choice)
            except:
                connection_label.config(text="connection: failed")

    def __init__(self, width=750, height=400, rows=100, columns=100):
        global connection_label
        root = Tk()
        # geeft een titel aan de window
        root.title("project 2.1")
        # geeft de window de grootte die aangegeven is
        root.geometry((str(width)+"x" + str(height)))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # makes frame waar alle elementen in komen
        frame = Frame(root, width=width, height=height)
        frame.grid(column=0, row=0, rowspan=rows, columnspan=columns, sticky=(N, S, E, W))

        connection_label = Label(frame, text="connection:")
        connection_label.grid(column=1, row=8)

        # creates the dropdown menu for the comports selecter, if it needs  to be updated this does that too
        def dropdown_menu():
            global com_port
            # maakt de com_port een stringvar in de root
            com_port = StringVar(root)
            # haalt alle compoorten op vanuit de functie get_com_ports in de linker.py en zet ze in een lijst
            com_port_choices = [get_com_ports()]
            # zet de default waarde voor de lijst
            com_port.set(com_port_choices[0])
            # maakt de dropdown menu waar je de compoorten kunt uitkiezen
            dropdownmenu = OptionMenu(frame, com_port, *com_port_choices)

            # plaats de dropdown menu in de grid
            dropdownmenu.grid(column=95, row=10, sticky="E,W")

        def close():
            add_task(close_connection, args=None, priority=1)
            connection_label.config(text="connection: closed")

        dropdown_menu()

        # maakt alle knoppen
        connect = Button(frame, text="open connection", command=lambda: background(self.connect))
        closeconn = Button(frame, text="close connection", command=lambda: add_task(close))
        refresh = Button(frame, text="refresh com ports", command=dropdown_menu)
        openblinds = Button(frame, text="open blinds", command=self.openblinds)
        closeblinds = Button(frame, text="close blinds", command=self.openblinds)

        # plaatst alle knoppen in de grid
        refresh.grid(column=95, row=9, sticky="E,W")
        connect.grid(column=95, row=11, sticky="E,W")
        closeconn.grid(column=95, row=12, sticky="E,W")
        openblinds.grid(column=95, row=80, sticky="E,W")
        closeblinds.grid(column=95, row=81, sticky="E,W")

        # maakt de canvassen
        canvas1 = Canvas(frame, width=ceil(width*0.1), height=ceil(height*0.3), bg='blue')
        canvas2 = Canvas(frame, width=ceil(width*0.1), height=ceil(height*0.3), bg='red')
        canvas3 = Canvas(frame, width=ceil(width*0.1), height=ceil(height*0.3), bg='green')

        ledstatus = Canvas(frame, width=20, height=20)
        ledstatus.create_oval(2, 2, 20, 20, fill="black")


        # plaats de canvassen
        canvas1.grid(column=2, row=70, sticky="N,S,E,W")
        canvas2.grid(column=3, row=70, sticky="N,S,E,W")
        canvas3.grid(column=4, row=70, sticky="N,S,E,W")
        ledstatus.grid(column=1, row=9, sticky="N,S,E,W")

        # zorgt voor het automatisch scalen van alle rows en colommen
        for i in range(columns):
            frame.columnconfigure(i, weight=1)
        for j in range(rows):
            frame.rowconfigure(j, weight=1)

        # zorgt voor mooi icoontje links bovenin
        root.iconbitmap('./python/windowicon.ico')

        root.mainloop()


def main():
    # maakt het object window
    Window()


if __name__ == '__main__':
    # runt de functie main direct na het uitvoeren van de code
    main()
