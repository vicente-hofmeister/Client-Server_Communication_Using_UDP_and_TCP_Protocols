from socket import *
class TCPclient:
      def __init__(self, serverAddress):
            self.serverAddress = serverAddress
            self.clientSocket = socket(AF_INET, SOCK_STREAM)
            self.clientSocket.settimeout(0.1)
            self.clientSocket.connect(self.serverAddress)

      # def start(self):
      #       self.clientSocket.connect((self.serverName,self.serverPort))
      #       sentence = input('Input lowercase sentence:')
      #       self.clientSocket.send(sentence.encode())
      #       modifiedSentence = self.clientSocket.recv(1024)
      #       print ('From Server:', modifiedSentence.decode())
      #       self.clientSocket.close()

      def changeServerAddress(self, newAddress):
            self.serverAddress = newAddress
            self.clientSocket.close()
            self.clientSocket = socket(AF_INET, SOCK_STREAM)
            self.clientSocket.settimeout(0.1)
            self.clientSocket.connect(self.serverAddress)
            # self.clientSocket.connect(newAddress)

      def sendMessage(self, message):
            self.clientSocket.send(message)
      
      def receiveMessage(self):
            serverMessage = self.clientSocket.recv(2048)
            return serverMessage, self.serverAddress
      
      def closeConnection(self):
            self.clientSocket.close()
