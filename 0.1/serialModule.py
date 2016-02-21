import serial
import thread
import threading
from utils import *

class SerialModule:
	def __init__(self):
		self.last_received = []
		self.timer = Timer()
		self.buffer_string = ""
	def ConnectTo(self, port , baudrate):
		self.timer.Reset()
		self.timer.Play()
		self.active = True
		self.blocked = False
		#thread.start_new_thread( self.ThreadRecv , (port,baudrate,))
		self.serial = serial.Serial(port , baudrate)
		self.port = port 
		self.baudrate = baudrate
		#self.start()

	
	def run(self):
		buffer_string = "first code\n"

		while self.active:
			buffer_string += self.serial.read(self.serial.inWaiting()) #read all char in buffer
        	while '\n' in buffer_string: #split data line by line and store it in var
				var, buffer_string = buffer_string.split('\n', 1)
				#time.sleep(0.01)
				self.last_received.append(var) #put received line in the queue
      	 	#time.sleep(0.01)
	def Kill(self):
		pass
	def GetData(self):
		#print "LAST RECV = " , self.last_received
		total = []
		last_received = self.last_received
		#print self.last_received
		self.last_received = []
		for x in range(len(last_received)):
			total.append(last_received[x])
		return total
	def Update(self):
		data = self.buffer_string + self.serial.read(self.serial.inWaiting())
		while '\n' in data:
			var , data = data.split('\n',1)
			self.last_received.append(var)
		self.buffer_string = data
	#def Update(self):
		#self.buffer_string += self.serial.read(self.serial.inWaiting()) #read all char in buffer
   #     data = self.buffer_string
    #    while '\n' in data: #split data line by line and store it in var
    #    	var, data = data.split('\n', 1)
     #   	self.last_received.append(var) #put received line in the queue
		#self.buffer_string = data
def main():
	testSerial = SerialModule()
	testSerial.ConnectTo('/dev/ttyACM0',57600)
	#time.sleep(5)
	ref = time.time()
	while time.time() - ref < 5:
		testSerial.Update()

	#testSerial.Kill()
	ref = time.time()
	
	while time.time() - ref < 1:
		testSerial.Update()

	data = testSerial.GetData()
	print data 
	testSerial.Kill()
	#time.sleep(2)

	#testSerial.ConnectTo('/dev/ttyACM0',57600)
	#time.sleep(5)
	#data = testSerial.GetData()
	#print data
	#testSerial.Kill()
	#time.sleep(2)

if __name__ == "__main__":
	main()