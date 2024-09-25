from socket import *
class TCPclient:
      def __init__(self, serverAddress):
            self.serverAddress = serverAddress
            self.clientSocket = socket(AF_INET, SOCK_STREAM)
            self.clientSocket.settimeout(0.1)
            self.clientSocket.connect(self.serverAddress)

      def changeServerAddress(self, newAddress):
            self.serverAddress = newAddress
            self.clientSocket.close()
            self.clientSocket = socket(AF_INET, SOCK_STREAM)
            self.clientSocket.settimeout(0.5)
            self.clientSocket.connect(self.serverAddress)

      def sendMessage(self, message):
            self.clientSocket.send(message)
      
      def receiveMessage(self):
            serverMessage = self.clientSocket.recv(2048)
            return serverMessage, self.serverAddress
      
      def closeConnection(self):
            self.clientSocket.close()
