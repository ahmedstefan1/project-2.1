import serial
import serial.tools.list_ports as com_ports

def get_com_ports():
    ports = list(com_ports.comports())
    formatted_comports = ports
    return formatted_comports


def serial_connection(COM):
    connection = serial.Serial(COM, 192000)
    print(connection)
    connection.write(b"t")
    while True:
        text = connection.read()
        print(text.hex())
