import serial
import serial.tools.list_ports as com_ports
import binascii
from Thread_management import *

connection = serial.Serial()


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
    getpacket()

# sluit de seriële connectie
def close_connection():
    global connection
    if connection.is_open:
        connection.close()
    else:
        print("no connection is open")

# leest de wat de arduino verstuurt
def getpacket():
    global connection
    while True:
        x = connection.readline()
        backgroundarg(protocol_understanding, (binascii.hexlify(x),))


# hoort characters te versturen
def sendpacket(data=hex(237)):
    global connection
    connection.write(data)


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
        # elif sensor =
        # elif sensor =

