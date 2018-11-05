from tkinter import *
from python.linker import *
from python.performance_management import *
from math import *


def open_blinds():
    close_blinds_command = bytes.fromhex("A01B0A")
    add_task(sendpacket, args=(close_blinds_command,), priority=2)


def close_blinds():
    open_blinds_command = bytes.fromhex("A0280A")
    add_task(sendpacket, args=(open_blinds_command,), priority=2)


class Window:
    com_port = None
    connection_label = Label

    # zorgt ervoor dat de verbinding word opgesteld
    @staticmethod
    def connect():
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
                clean_queue()

    def __init__(self, width=1200, height=750, rows=100, columns=100):
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

        connection_label = Label(frame, text="connection: Status")
        connection_label.grid(column=1, row=8, sticky="E,W")

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
        closeconn = Button(frame, text="close connection", command=lambda: background(close))
        refresh = Button(frame, text="refresh com ports", command=dropdown_menu)
        openblinds = Button(frame, text="open blinds", command=lambda: background(open_blinds))
        closeblinds = Button(frame, text="close blinds", command=lambda: background(close_blinds))

        # plaatst alle knoppen in de grid
        refresh.grid(column=95, row=9, sticky="E,W")
        connect.grid(column=95, row=11, sticky="E,W")
        closeconn.grid(column=95, row=12, sticky="E,W")
        openblinds.grid(column=95, row=80, sticky="E,W")
        closeblinds.grid(column=95, row=81, sticky="E,W")

        canvas1 = Canvas(frame, bd=0, highlightthickness=0, bg="white")
        canvas2 = Canvas(frame, bd=0, highlightthickness=0, bg="blue")
        canvas3 = Canvas(frame, bd=0, highlightthickness=0, bg="green")

        # TODO add comments
        def configure(event):
            canvas1.delete("all")
            canvas1.config(width=ceil(frame.winfo_width() * 0.4), height=ceil(frame.winfo_height() * 0.3))
            canvas2.config(width=ceil(frame.winfo_width() * 0.4), height=ceil(frame.winfo_height() * 0.3))
            canvas3.config(width=ceil(frame.winfo_width() * 0.4), height=ceil(frame.winfo_height() * 0.3))
            w, h = event.width, event.height
            canvas1.create_line((w * 0.9), (h * 0.9), (w * 0.2), (h * 0.9), width=2, tags="x-as", fill="black")
            canvas1.create_line((w * 0.2), (h * 0.1), (w * 0.2), (h * 0.9), width=2, tags="y-as", fill="black")
            canvas1.create_text((w * 0.1), (h * 0.5), text='waarde', anchor=N, tags="line")
            canvas1.create_text((w * 0.5), (h * 0.95), text='time', anchor=N, tags="line")

            for i in range(11):
                x = i * (w * 0.7 * 0.1) + (w * 0.2)
                canvas1.create_line(x, (h * 0.89), x, (h * 0.1), width=1, dash=(2, 5))
                canvas1.create_text(x, (h * 0.90), text='%d' % (10 * i), anchor=N)

            for j in range(11):
                if j > 0:
                    y = h - j * (h * 0.8 * 0.1) - (h * 0.1)
                    canvas1.create_line((w * 0.2), y, (w * 0.9), y, width=1, dash=(2, 5))
                    canvas1.create_text((w * 0.18), y, text='%d' % (10 * j), anchor=N)

            canvas2.delete("all")
            w, h = event.width, event.height
            canvas2.create_line((w * 0.9), (h * 0.9), (w * 0.2), (h * 0.9), width=2, tags="x-as", fill="black")
            canvas2.create_line((w * 0.2), (h * 0.1), (w * 0.2), (h * 0.9), width=2, tags="y-as", fill="black")
            canvas2.create_text((w * 0.1), (h * 0.5), text='waarde', anchor=N, tags="line")
            canvas2.create_text((w * 0.5), (h * 0.95), text='time', anchor=N, tags="line")

            for i in range(11):
                x = i * (w * 0.7 * 0.1) + (w * 0.2)
                canvas2.create_line(x, (h * 0.89), x, (h * 0.1), width=1, dash=(2, 5))
                canvas2.create_text(x, (h * 0.90), text='%d' % (10 * i), anchor=N)

            for j in range(11):
                if j > 0:
                    y = h - j * (h * 0.8 * 0.1) - (h * 0.1)
                    canvas2.create_line((w * 0.2), y, (w * 0.9), y, width=1, dash=(2, 5))
                    canvas2.create_text((w * 0.18), y, text='%d' % (10 * j), anchor=N)

            canvas3.delete("all")
            w, h = event.width, event.height
            canvas3.create_line((w * 0.9), (h * 0.9), (w * 0.2), (h * 0.9), width=2, tags="x-as", fill="black")
            canvas3.create_line((w * 0.2), (h * 0.1), (w * 0.2), (h * 0.9), width=2, tags="y-as", fill="black")
            canvas3.create_text((w * 0.1), (h * 0.5), text='waarde', anchor=N, tags="line")
            canvas3.create_text((w * 0.5), (h * 0.95), text='time', anchor=N, tags="line")

            for i in range(11):
                x = i * (w * 0.7 * 0.1) + (w * 0.2)
                canvas3.create_line(x, (h * 0.89), x, (h * 0.1), width=1, dash=(2, 5))
                canvas3.create_text(x, (h * 0.90), text='%d' % (10 * i), anchor=N)

            for j in range(11):
                if j > 0:
                    y = h - j * (h * 0.8 * 0.1) - (h * 0.1)
                    canvas3.create_line((w * 0.2), y, (w * 0.9), y, width=1, dash=(2, 5))
                    canvas3.create_text((w * 0.18), y, text='%d' % (10 * j), anchor=N)

        canvas1.bind("<Configure>", configure)
        canvas2.bind("<Configure>", configure)
        canvas3.bind("<Configure>", configure)

        canvas1.grid(row=70, column=4)
        canvas2.grid(row=71, column=4)
        canvas3.grid(row=71, column=5)

        ledstatus = Canvas(frame, width=20, height=20)
        ledstatus.create_oval(2, 2, 20, 20, fill="black", tags="ledstatus")

        # changes the led status in the gui
        def updateled():
            # gets the color value from the function in linker
            color = get_led()
            if color == 1:
                ledstatus.create_oval(2, 2, 20, 20, fill="green", outline="green", tags="ledstatus")
            elif color == 2:
                ledstatus.create_oval(2, 2, 20, 20, fill="yellow", outline="yellow", tags="ledstatus")
            elif color == 3:
                ledstatus.create_oval(2, 2, 20, 20, fill="red", outline="red", tags="ledstatus")
            # runs the updater again and changes the color
            ledstatus.after(1000, updateled)

        # runs updateled in een andere thread
        backgroundarg(ledstatus.after, (1000, updateled,))

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
