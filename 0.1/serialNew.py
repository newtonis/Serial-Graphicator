import sys
import thread
import time
from urlparse import urlparse
from twisted.web import server, resource
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.serialport import SerialPort

serServ = None

class USBclient(Protocol):
    def connectionMade(self):
        global serServ
        serServ = self
        print 'Arduino device: ', serServ, ' is connected.'

    def cmdReceived(self, cmd):
        serServ.transport.write(cmd)
        print cmd, ' - sent to Arduino.'
        pass

    def dataReceived(self,data):      
        print 'USBclient.dataReceived called with:'
        print data

class HTTPserver(resource.Resource):
    isLeaf = True
    def render_GET(self, request):      #passes the data from the get request
        print 'HTTP request received'
        myArduino = USBclient()
        stringit = str(request)
        parse = stringit.split()
        command, path, version = parse
        myArduino.cmdReceived(path)

class cmdTransport(Protocol):
    def __init__(self, factory):
        self.factory = factory

class SerialModule:
    def __init__(self):
        self.HTTPsetup = server.Site(HTTPserver())
        reactor.listenTCP(5000, HTTPsetup)
        SerialPort(USBclient(), '/dev/ttyACM0', reactor, baudrate='57600')
        thread.start_new_thread( reactor.run , ())

def main():
    HTTPsetup = server.Site(HTTPserver())
    reactor.listenTCP(5000, HTTPsetup)
    SerialPort(USBclient(), '/dev/ttyACM0', reactor, baudrate='57600')
    reactor.run()
    #thread.start_new_thread( reactor.run , ())

    #time.sleep(5)
if __name__ == "__main__":
    main()