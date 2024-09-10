from socket import *
class TCPclient:
      def __init__(self, serverName, serverPort):
            self.serverName = serverName
            self.serverPort = serverPort
            self.clientSocket = socket(AF_INET, SOCK_STREAM)
      
      def start(self):
            self.clientSocket.connect((self.serverName,self.serverPort))
            sentence = input('Input lowercase sentence:')
            self.clientSocket.send(sentence.encode())
            modifiedSentence = self.clientSocket.recv(1024)
            print ('From Server:', modifiedSentence.decode())
            self.clientSocket.close()
