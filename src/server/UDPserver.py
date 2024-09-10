from socket import *
from utils import server_utils as utils

class UDPserver:
      def __init__(self,serverPort):
            self.serverPort = serverPort
            self.serverSocket = socket(AF_INET, SOCK_DGRAM)
            self.serverSocket.bind(('', self.serverPort))
            print ('The UDP server is ready to receive')

      def start(self):
            while True:
                  messageFromClient, clientAddress = self.serverSocket.recvfrom(2048)
                  message, address = utils.handleMessage(messageFromClient= messageFromClient, clientAddress= clientAddress)

                  self.serverSocket.sendto(message,address)