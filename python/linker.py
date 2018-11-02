import serial
import serial.tools.list_ports as com_ports
import binascii
from python.performance_management import *
from sched import *
from time import *


connection = serial.Serial()
s = scheduler(time, sleep)
ranonce = False



# haalt op wat voor comports zijn aangesloten op de PC
def get_com_ports():
    ports = list(com_ports.comports())
    formatted_comports = []
    print(len(ports))
    for p in ports:
        formatted_comports.append(p[0])
    print(formatted_comports)
    if len(ports) < 1:
        return "N/A"
    else:
        return formatted_comports


# maakt de seriele connectie
def serial_connection(com):
    global connection
    connection = serial.Serial(com, 19200)
    print(connection)
    add_task()


# sluit de seriële connectie
def close_connection():
    global connection
    for task in s.queue:
        s.cancel(task)

    print(s.empty())
    if connection.is_open and s.empty():
        connection.close()
    else:
        print("no connection is open")
    add_task(end_thread,None,4)


# leest de wat de arduino verstuurt
def getpacket():
    global connection
    x = connection.readline()
    try:
        protocol_understanding(binascii.hexlify(x))
    except:
        print("guess what again")


# hoort characters te versturen
def sendpacket(data=hex(237)):
    global connection
    connection.write(data)


def addself():
    s.enter(0.2, 2, add_task)
    s.enter(0.3, 3, addself)


# adds tasks
def add_task(task=getpacket, args=None , priority= 2):
    # als er geen argumenten zijn gegeven hoeven die niet erbij
    if not ranonce:
        addself()
    if args is None:
        s.enter(0.1, priority, task)
    else:
        s.enter(0.1, priority, task, argument=args)
    # zorgt ervoor dat deze taak zichzelf oproept zodat je niet alleen 1 keer de getpackets uitvoert
    # voert de taken uit
    s.run()


# understands the protocol and checks for mistakes
def protocol_understanding(data):
    # slices the data to what is needed
    sliced_data = data[0:4]

    # puts the data in different variables
    sensor = sliced_data[0:1]
    waarde = sliced_data[1:3]
    check = sliced_data[3:4]
    # xors the front part of the data with the back part, er is wat omrekenen nodig
    # Xor werkt alleen met Int en niet met hexadecimalen
    U1 = int(waarde[0:1], 16) ^ int(waarde[1:2], 16)
    # xors de data van de sensor met uitkomst1 (U1)
    U2 = U1 ^ int(sensor, 16)
    # kijkt of die waarden overeen komen ( als ze niet overeen komen is er waarschijnlijk ergens een fout ontstaan
    if U2 == int(check, 16):
        # welke sensor komt het uit
        if sensor == b'8':
            # print de waarde van de sensor naar de console
            print("temperatuur:" + str(int(waarde, 16)) + u'\u00B0' + "C")
        # elif sensor =
            # print("temperatuur:" + str(int(waarde, 16)) + u'\u00B0' + "C")
        # elif sensor =
            # print("temperatuur:" + str(int(waarde, 16)) + u'\u00B0' + "C")
        # elif sensor =
            # print("temperatuur:" + str(int(waarde, 16)) + u'\u00B0' + "C")
        else:
            print("something went wrong")

    else:
        print("didnt pass check")

