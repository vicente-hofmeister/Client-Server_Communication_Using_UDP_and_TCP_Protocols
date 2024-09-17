from socket import *

class UDPserver:
      def __init__(self,serverPort):
            self.serverPort = serverPort
            self.serverSocket = socket(AF_INET, SOCK_DGRAM)
            self.serverSocket.bind(('', self.serverPort))
            print ('The UDP server is ready to receive')

      def receiveMessage(self):
            return self.serverSocket.recvfrom(2048)
      
      def sendMessage(self, message, address):
            self.serverSocket.sendto(message, address)