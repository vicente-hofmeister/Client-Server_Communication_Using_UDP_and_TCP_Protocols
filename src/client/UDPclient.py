from socket import *
class UDPclient:
      def __init__(self, serverAddress):
            self.serverAddress = serverAddress
            self.clientSocket = socket(AF_INET, SOCK_DGRAM)
            self.clientSocket.settimeout(0.5)

      def changeServerAddress(self, newAddress):
            self.serverAddress = newAddress

      def sendMessage(self, message):
            self.clientSocket.sendto(message, self.serverAddress)

      def receiveMessage(self):
            serverMessage = self.clientSocket.recvfrom(2048)
            return serverMessage

      def closeConnection(self):
            self.clientSocket.close()