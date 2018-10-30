import serial
import serial.tools.list_ports as com_ports


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
    connection = serial.Serial(com, 19200)
    print(connection)
    while True:
        print(connection.read())
