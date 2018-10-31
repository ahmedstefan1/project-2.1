import serial
import serial.tools.list_ports as com_ports

connection = serial.Serial()
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


def serial_connection(com):
    global connection
    connection.port(com)
    connection.baudrate(19200)
    print(connection)


def close_connection():
    global connection
    if connection.is_open:
        connection.close()
    else:
        print("no connection is open")


def read():
    global connection
    connection.open()
    while True:
        print(hex(connection.read))


def send(data):
    global connection
    connection.write(data)
