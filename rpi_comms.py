import serial

def rpi_write(message: str):
    if len(message) == 0 or message[-1] != "\n":
        message = message + "\n"
    if ser.is_open:
        ser.write(message.encode())

def rpi_read():
    if ser.is_open:
        return ser.readline().decode()

while True:
    message = input("Type a message:\n")
    try: 
        # Set up serial port
        ser = serial.Serial("/dev/tty.usbmodem2101", 115200, timeout=5)

        rpi_write(message)
        print(rpi_read())
        
        ser.close()
    except:
        print("Serial port is unconnected")
