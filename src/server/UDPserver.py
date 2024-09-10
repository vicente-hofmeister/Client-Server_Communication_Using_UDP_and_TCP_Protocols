from socket import *

class UDPserver:
      def __init__(self,serverPort):
            self.serverPort = serverPort
            self.serverSocket = socket(AF_INET, SOCK_DGRAM)
            self.serverSocket.bind(('', self.serverPort))
            print ('The UDP server is ready to receive')

      def start(self):
            while True:
                  messageFromClient1, client1Address = self.serverSocket.recvfrom(2048)
                  messageFromClient2, client2Address = self.serverSocket.recvfrom(2048)

                  self.serverSocket.sendto(messageFromClient2,client1Address)
                  self.serverSocket.sendto(messageFromClient1,client2Address)