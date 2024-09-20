from socket import *

class UDPserver:
      def __init__(self,serverPort):
            self.serverPort = serverPort
            self.masterSocket = socket(AF_INET, SOCK_DGRAM)
            self.masterSocket.bind(('', self.serverPort))
            self.socketList = []
            print ('The UDP server is ready to receive')

      def newSocket(self):
            clientSocket = socket(AF_INET, SOCK_DGRAM)
            clientSocket.bind(('', (self.serverPort + 1 + len(self.socketList))))

      def receiveMessage(self):
            return self.masterSocket.recvfrom(2048)
      
      def sendMessage(self, message, address):
            self.masterSocket.sendto(message, address)