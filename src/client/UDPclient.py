from socket import *
import threading

from utils import client_utils as utils

class UDPclient:
      def __init__(self, serverName, serverPort):
            self.serverName = serverName
            self.serverPort = serverPort
            self.clientSocket = socket(AF_INET, SOCK_DGRAM)

      def send_connect():
            client_response = utils.choose_firend()
            

      def start(self):

            messageToRegister = utils.initialize_client()
            self.clientSocket.sendto(messageToRegister, (self.serverName, self.serverPort))
            self.clientSocket.recvfrom(2048)

            send_connect_thread = threading.Thread(target=utils.choose_firend)
            receive_connect_thread = threading.Thread(target= utils.manageResponse, args= self.clientSocket.recvfrom(2048))

            send_connect_thread.start()
            receive_connect_thread.start()

            # send_thread = threading.Thread(target= , args= )
            # receive_thread = threading.Thread(target= utils.manageResponse, args= self.clientSocket.recvfrom(2048))



            while True:
                  messageToServer, address = utils.manageResponse(self.clientSocket.recvfrom(2048))

                  self.clientSocket.sendto(messageToServer, address)

                  # friendName = names[1]
                  # message = input('What do you want to say?')
                  # messageToServer= "[{},{},{}]".format(myName, friendName, message)

                  # self.clientSocket.sendto(messageToServer.encode(), (self.serverName, self.serverPort))

                  # recievedMessage, serverAddress = self.clientSocket.recvfrom(2048)


            self.clientSocket.close()