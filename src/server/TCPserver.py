from socket import *

class TCPserver:
      def __init__(self, serverPort):
            self.serverPort = serverPort
            self.serverSocket = socket(AF_INET,SOCK_STREAM)
            self.serverSocket.bind(('',self.serverPort))
            self.serverSocket.listen(1)
            print ('The TCP server is ready to receive')


      def start(self):
            while True:
                  connectionSocket, addr = self.serverSocket.accept()
                  sentence = connectionSocket.recv(1024).decode()
                  capitalizedSentence = sentence.upper()
                  connectionSocket.send(capitalizedSentence.encode())
                  connectionSocket.close()