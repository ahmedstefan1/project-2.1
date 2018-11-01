import serial
import serial.tools.list_ports as com_ports

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
    readlines()

# sluit de seriële connectie
def close_connection():
    global connection
    if connection.is_open:
        connection.close()
    else:
        print("no connection is open")

# leest de wat de arduino verstuurt
def readlines():
    global connection
    while True:
        x = connection.read()
        print(x)

# hoort characters te versturen
def send(data=hex(237)):
    global connection
    connection.write(data)
