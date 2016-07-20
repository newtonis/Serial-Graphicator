import serial
import thread
ser = serial.Serial('/dev/ttyACM0', 57600)
last_received = []

def receiving(ser):
    global last_received

    buffer_string = ''
    while True:
        buffer_string = buffer_string + ser.read(ser.inWaiting())
        if '\n' in buffer_string:
            lines = buffer_string.split('\n') # Guaranteed to have at least 2 entries
            last_received.append( lines[-2] )
            #If the Arduino sends lots of empty lines, you'll lose the
            #last filled line, so you could make the above statement conditional
            #like so: if lines[-2]: last_received = lines[-2]
            buffer_string = lines[-1]

thread.start_new_thread(receiving,(ser,))

while True:
    for x in range(len(last_received)):
        print last_received[x]
	
#receiving(ser)
#while True:
	
	#print ser.readline()