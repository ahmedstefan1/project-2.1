import serial
import serial.tools.list_ports as com_ports
import binascii
from sched import *
from time import *


connection = serial.Serial()
s = scheduler(time, sleep)
ran_once = False
used_com = None
color_led = None
new_color = None

temperature = None
distance = None
light_intensity = None


# haalt op wat voor comports zijn aangesloten op de PC
def get_com_ports():
    ports = list(com_ports.comports())
    formatted_comports = []
    for p in ports:
        formatted_comports.append(p[0])
    if len(ports) < 1:
        return "N/A"
    else:
        return formatted_comports


# maakt de seriele connectie
def serial_connection(com):
    global connection, used_com
    used_com = com
    connection = serial.Serial(com, 19200)
    add_task()


def clean_queue():
    try:
        for task in s.queue:
            s.cancel(task)
    except:
        print("cleaned")


# sluit de seriële connectie
def close_connection():
    global connection
    clean_queue()

    if connection.is_open and s.empty():
        connection.close()
    else:
        print("no connection is open")


# leest de wat de arduino verstuurt
def getpacket():
    global connection
    x = connection.readline()
    try:
        protocol_understanding(binascii.hexlify(x))
    except:
        print("it happened again")


# resets connection
def reset():
    global ran_once, used_com
    ran_once = False
    close_connection()
    serial_connection(used_com)


# hoort characters te versturen
def sendpacket(data=None):
    global connection
    clean_queue()
    print(data)
    connection.write(data)
    reset()


def addself():
    s.enter(0.2, 3, add_task)
    s.enter(1, 4, addself)


# adds tasks
def add_task(task=getpacket, priority=3, args=None):
    # als er geen argumenten zijn gegeven hoeven die niet erbij
    if not ran_once:
        addself()
    if args is None:
        s.enter(0.2, priority, task)
    else:
        s.enter(0.2, priority, task, argument=args)
    # zorgt ervoor dat deze taak zichzelf oproept zodat je niet alleen 1 keer de getpackets uitvoert
    # voert de taken uit
    s.run()


def get_led():
    global color_led, new_color
    if color_led == new_color:
        return color_led
    else:
        color_led = new_color
        return color_led


def get_temp():
    global temperature
    return temperature


def get_light():
    global light_intensity
    return light_intensity


def get_distance():
    global distance
    return distance


def end():
    global distance, light_intensity, temperature
    distance = light_intensity  = 0
    temperature = 30


# understands the protocol and checks for mistakes
def protocol_understanding(data):
    global new_color, temperature, distance, light_intensity
    # slices the data to what is needed
    sliced_data = data[0:4]

    # puts the data in different variables
    type_data = sliced_data[0:1]
    waarde = sliced_data[1:3]
    check = sliced_data[3:4]
    # xors the front part of the data with the back part, er is wat omrekenen nodig
    # Xor werkt alleen met Int en niet met hexadecimalen
    u1 = int(waarde[0:1], 16) ^ int(waarde[1:2], 16)
    # xors de data van de type_data met uitkomst1 (u1)
    u2 = u1 ^ int(type_data, 16)
    # kijkt of die waarden overeen komen ( als ze niet overeen komen is er waarschijnlijk ergens een fout ontstaan
    if u2 == int(check, 16):
        # welke type_data komt het uit
        if type_data == b'8':
            # print de waarde van de type_data naar de console
            temperature = int(waarde, 16)
        elif type_data == b'1':
            new_color = int(waarde, 16)
        elif type_data == b'2':
            distance = int(waarde, 16)
        elif type_data == b'4':
            light_intensity = int(waarde, 16)
        # elif type_data ==
            # print("type_data:" + str(int(waarde, 16)) + "eenheid")
