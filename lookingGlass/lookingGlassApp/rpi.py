import serial

NUM_READS = 5
DEBUG = True

# Write to serial port
def write(ser):
    message = "Hi\n"
    if ser.is_open:
        ser.write(message.encode())
        print("Sending")

# Read from serial port
def read(ser):
    if ser.is_open:
        return ser.readline().decode()

# Find most frequent element in a list
def most_frequent(List):
    return max(set(List), key = List.count)

def getUser():
    print("calling getUser")
    try:
        # Set up serial port
        ser = serial.Serial("/dev/tty.usbmodem2101", 115200, timeout=1)
    
        names = []
        for i in range(NUM_READS):
            write(ser)
            result = read(ser)
            if DEBUG: 
                print(result)
            names.append(result)
        
        user = most_frequent(names)
        
        if DEBUG: 
            print("Most frequent: " + user)

        ser.close()
        return user
    
    except:
        print("Serial port is unconnected")
        return "Unknown"