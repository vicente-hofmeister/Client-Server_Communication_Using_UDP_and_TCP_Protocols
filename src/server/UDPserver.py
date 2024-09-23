from socket import *

class UDPserver:
      def __init__(self,serverPort,client):
            self.serverPort = serverPort
            self.serverSocket = socket(AF_INET, SOCK_DGRAM)
            self.serverSocket.bind(('', self.serverPort))
            self.serverSocket.settimeout(0.1)
            self.client = client

      def receiveMessage(self):
            clientMessage =  self.serverSocket.recvfrom(2048)
            return clientMessage
      def sendMessage(self, message, address):
            self.serverSocket.sendto(message, address)

      def getClient(self):
            return self.client

      # def closeSocket(self, ):
