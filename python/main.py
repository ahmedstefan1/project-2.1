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
                end()
                clean_queue()

    def __init__(self, width=850, height=500, rows=100, columns=100):
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

        # maakt legenda voor LED-status
        connection_label = Label(frame, text="Connection: Status")
        connection_label.grid(column=1, row=8, sticky="W")

        legenda_label = Label(frame, text="Legenda LED-status:")
        legenda_label.grid(column=1, row=10, sticky="W")

        blinds_open_label = Label(frame, text="Scherm is uitgerold", bg="red")
        blinds_open_label.grid(column=1, row=11, sticky="W")

        blinds_closing_label = Label(frame,text="Scherm wordt in- of uitgerold", bg="yellow")
        blinds_closing_label.grid(column=1, row=12, sticky="W")

        blinds_closed_label = Label(frame, text="Scherm is ingerold", bg="green")
        blinds_closed_label.grid(column=1, row=13, sticky="W")

        # maakt textvak voor inkomende temperatuur
        tekstvak = Text(frame, height=9, width=30)
        tekstvak.grid(column=5, row=70, sticky="W,E")
        tekstvak.insert(INSERT, "Waardes op dit moment: \n"
                        "Temperatuur (\u00B0C): ", str(get_temp()), "\n"
                        "Afstand (cm): ", str(get_distance()), "\n"
                        "Licht (%): ", str(get_light()))

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
            end()

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

        # maakt alle canvassen
        canvas1 = Canvas(frame, bd=0, highlightthickness=0, bg="white")
        canvas2 = Canvas(frame, bd=0, highlightthickness=0, bg="white")
        canvas3 = Canvas(frame, bd=0, highlightthickness=0, bg="white")

        # geeft de canvas een dynamische grootte
        def configure(event):
            canvas1.delete("all")
            canvas2.delete("all")
            canvas3.delete("all")
            # geeft de grootte van de canvassen
            canvas1.config(width=ceil(frame.winfo_width() * 0.35), height=ceil(frame.winfo_height() * 0.3))
            canvas2.config(width=ceil(frame.winfo_width() * 0.35), height=ceil(frame.winfo_height() * 0.3))
            canvas3.config(width=ceil(frame.winfo_width() * 0.35), height=ceil(frame.winfo_height() * 0.3))

            # zet de groote in variabelen
            w, h = event.width, event.height

            # tekent alle lijnen voor canvas 1
            canvas1.create_line((w * 0.9), (h * 0.9), (w * 0.2), (h * 0.9), width=2, tags="x-as", fill="black")
            canvas1.create_line((w * 0.2), (h * 0.1), (w * 0.2), (h * 0.9), width=2, tags="y-as", fill="black")
            canvas1.create_text((w * 0.5), (h * 0.01), text='temperatuur', anchor=N, tags="line")
            canvas1.create_text((w * 0.1), (h * 0.5), text=(u'\u00B0' + "C"), anchor=N, tags="temp")
            canvas1.create_text((w * 0.5), (h * 0.95), text='time', anchor=N, tags="temp")

            # tekent alle stippenlijnen en text voor canvas 1
            for a in range(11):
                x = a * (w * 0.7 * 0.1) + (w * 0.2)
                canvas1.create_line(x, (h * 0.89), x, (h * 0.1), width=1, dash=(2, 5))
                canvas1.create_text(x, (h * 0.90), text='%d' % (10 * a), anchor=N)

            for b in range(11):
                y = h - b * (h * 0.8 * 0.1) - (h * 0.1)
                canvas1.create_line((w * 0.2), y, (w * 0.9), y, width=1, dash=(2, 5))
                canvas1.create_text((w * 0.17), (y-10), text='%d' % (10 * (b-3)), anchor=N)

            # tekent alle lijnen en text voor canvas 2
            canvas2.create_line((w * 0.9), (h * 0.9), (w * 0.2), (h * 0.9), width=2, tags="x-as", fill="black")
            canvas2.create_line((w * 0.2), (h * 0.1), (w * 0.2), (h * 0.9), width=2, tags="y-as", fill="black")
            canvas2.create_text((w * 0.5), (h * 0.01), text='afstand', anchor=N, tags="temp")
            canvas2.create_text((w * 0.1), (h * 0.5), text='CM', anchor=N, tags="temp")
            canvas2.create_text((w * 0.5), (h * 0.95), text='time', anchor=N, tags="temp")

            # tekent alle stippenlijnen voor canvas 2
            for c in range(11):
                x = c * (w * 0.7 * 0.1) + (w * 0.2)
                canvas2.create_line(x, (h * 0.89), x, (h * 0.1), width=1, dash=(2, 5))
                canvas2.create_text(x, (h * 0.90), text='%d' % (10 * c), anchor=N)

            for d in range(11):
                if d > 0:
                    y = h - d * (h * 0.8 * 0.1) - (h * 0.1)
                    canvas2.create_line((w * 0.2), y, (w * 0.9), y, width=1, dash=(2, 5))
                    canvas2.create_text((w * 0.17), y-10, text='%d' % (10 * d), anchor=N)

            # maakt alle normale lijnen en text voor canvas 3
            canvas3.create_line((w * 0.9), (h * 0.9), (w * 0.2), (h * 0.9), width=2, tags="x-as", fill="black")
            canvas3.create_line((w * 0.2), (h * 0.1), (w * 0.2), (h * 0.9), width=2, tags="y-as", fill="black")
            canvas3.create_text((w * 0.5), (h * 0.01), text='licht', anchor=N, tags="temp")
            canvas3.create_text((w * 0.1), (h * 0.5), text='%', anchor=N, tags="temp")
            canvas3.create_text((w * 0.5), (h * 0.95), text='time', anchor=N, tags="temp")

            # maakt alle stippenlijnen voor canvas 3
            for e in range(11):
                x = e * (w * 0.7 * 0.1) + (w * 0.2)
                canvas3.create_line(x, (h * 0.89), x, (h * 0.1), width=1, dash=(2, 5))
                canvas3.create_text(x, (h * 0.90), text='%d' % (10 * e), anchor=N)

            for f in range(11):
                if f > 0:
                    y = h - f * (h * 0.8 * 0.1) - (h * 0.1)
                    canvas3.create_line((w * 0.2), y, (w * 0.9), y, width=1, dash=(2, 5))
                    canvas3.create_text((w * 0.17), y-10, text='%d' % (10 * f), anchor=N)

        # zorgt ervoor dat de 3 canvassen aan de functie configure aangesloten zijn
        canvas1.bind("<Configure>", configure)
        canvas2.bind("<Configure>", configure)
        canvas3.bind("<Configure>", configure)

        temp_x2 = None
        temp_y2 = None
        temp_s = 0

        def create_lines_temp():
            nonlocal temp_s, temp_x2, temp_y2
            # haalt de lengte en breedte op van de canvas
            width = int(canvas1.cget("width"))
            height = int(canvas1.cget("height"))
            # als hij al 10 lijntjes heeft getekent start hij opniew en zet de waarden op standaard
            if temp_s >= 10:
                temp_s = 0
                temp_x2 = int(canvas1.cget("width")) * 0.2
                canvas1.delete('line')
                print("reset")
            # als de temperatuur x2 niks is dan haalt hij de breedte op van de canvas
            if temp_x2 is None:
                temp_x2 = int(canvas1.cget("width")) * 0.2

            # haalt de temperatuur op
            if get_temp() is not None:
                temp = get_temp()
                print(temp)
                if temp_y2 is None:
                    temp_y2 = (height * 0.9) - (height * 0.8 / 100 * temp)
                # wat rekenen is nodig voor het goed zetten van de lijn
                x1 = temp_x2 + (width * 0.7 * 0.1)
                y1 = (height * 0.9) - (height * 0.8 / 100 * temp)
                # tekent de lijn
                canvas1.create_line(x1, y1, temp_x2, temp_y2, fill='blue', tags='line', width=2)

                temp_x2 = x1
                temp_y2 = y1
                temp_s += 1
            canvas1.after(1000, create_lines_temp)

        light_x2 = None
        light_y2 = None
        light_s = 0

        def create_lines_light():
            nonlocal light_s, light_x2, light_y2
            # haalt de lengte en breedte op van de canvas
            width = int(canvas3.cget("width"))
            height = int(canvas3.cget("height"))
            # als hij al 10 lijntjes heeft getekent start hij opniew en zet de waarden op standaard
            if light_s >= 10:
                light_s = 0
                light_x2 = int(canvas3.cget("width"))*0.2
                canvas3.delete('line')
                print("reset")
            # als de temperatuur x2 niks is dan haalt hij de breedte op van de canvas
            if light_x2 is None:
                light_x2 = int(canvas3.cget("width")) * 0.2
            # haalt de licht intensiteit op
            if get_light() is not None:
                light = get_light()
                print(light)
                if light_y2 is None:
                    light_y2 = (height*0.9)-(height*0.8/100*light)
                # wat rekenen is nodig voor het goed zetten van de lijn
                x1 = light_x2 + (width*0.7*0.1)
                y1 = (height*0.9)-(height*0.8/100*light)
                # tekent de lijn
                canvas3.create_line(x1, y1, light_x2, light_y2, fill='blue', tags='line', width=2)
                light_x2 = x1
                light_y2 = y1
                light_s += 1
            canvas3.after(1000, create_lines_light)

        distance_x2 = None
        distance_y2 = None
        distance_s = 0

        def create_lines_distance():
            nonlocal distance_s, distance_x2, distance_y2
            # haalt de lengte en breedte op van de canvas
            width = int(canvas2.cget("width"))
            height = int(canvas2.cget("height"))
            # als hij al 10 lijntjes heeft getekent start hij opnieuw en zet de waarden op standaard
            if distance_s >= 10:
                distance_s = 0
                distance_x2 = int(canvas2.cget("width")) * 0.2
                canvas2.delete('line')
                print("reset")
            # als de distance x2 niks is dan haalt hij de breedte op van de canvas
            if distance_x2 is None:
                distance_x2 = int(canvas2.cget("width")) * 0.2
            # haalt de afstand op
            if get_distance() is not None:
                distance = get_distance()
                print(distance)
                if distance_y2 is None:
                    distance_y2 = (height * 0.9) - (height * 0.8 / 100 * distance)
                # wat rekenen is nodig voor het goed zetten van de lijn
                x1 = distance_x2 + (width * 0.7 * 0.1)
                y1 = (height * 0.9) - (height * 0.8 / 100 * distance)
                # tekent de lijn
                canvas2.create_line(x1, y1, distance_x2, distance_y2, fill='blue', tags='line', width=2)
                distance_x2 = x1
                distance_y2 = y1
                distance_s += 1
            canvas2.after(1000, create_lines_distance)

        backgroundarg(canvas1.after, (1000, create_lines_temp,))
        backgroundarg(canvas3.after, (1000, create_lines_light,))
        backgroundarg(canvas2.after, (1000, create_lines_distance,))

        # plaatst de canvassen in een grid
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
       # root.iconbitmap('./python/windowicon.ico')

        root.mainloop()


def main():
    # maakt het object window
    Window()


if __name__ == '__main__':
    # runt de functie main direct na het uitvoeren van de code
    main()
