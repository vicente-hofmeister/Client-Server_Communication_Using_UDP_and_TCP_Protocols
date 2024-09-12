import ast
from socket import *
import threading

from utils import client_utils as utils

class UDPclient:
      def __init__(self, serverName, serverPort):
            self.serverName = serverName
            self.serverPort = serverPort
            self.socket1 = socket(AF_INET, SOCK_DGRAM)
            self.socket2 = socket(AF_INET, SOCK_DGRAM)

      def start(self):
            
            def sendConnect():
                  clientMessage, serverAddress = utils.choose_friend()
                  self.clientSocket.sendto(clientMessage, serverAddress)
                  response = utils.manage_response(self.socket1.recvfrom(2048))

                  if type(response) == "str":
                        if response == "accepted":
                              return
            
            def waitMessage():
                  utils.manage_response(self.socket2.recvfrom(2048))


            clientMessage = utils.initialize_client()
            self.socket1.sendto(clientMessage, (self.serverName, self.serverPort))
            serverMessage = self.socket1.recvfrom(2048)
            registered = utils.check_register(serverMessage)

            if not registered:
                  self.socket1.close()
                  return

            sendConnectThread = threading.Thread(target=sendConnect)
            receiveConnectThread = threading.Thread(target= utils.manage_response, args= self.clientSocket.recvfrom(2048))

            sendConnectThread.start()
            receiveConnectThread.start()

            # send_thread = threading.Thread(target= , args= )
            # receive_thread = threading.Thread(target= utils.manage_response, args= self.clientSocket.recvfrom(2048))



            # while True:
            #       messageToServer, address = utils.manage_response(self.clientSocket.recvfrom(2048))

            #       self.clientSocket.sendto(messageToServer, address)

                  # friendName = names[1]
                  # message = input('What do you want to say?')
                  # messageToServer= "[{},{},{}]".format(myName, friendName, message)

                  # self.clientSocket.sendto(messageToServer.encode(), (self.serverName, self.serverPort))

                  # recievedMessage, serverAddress = self.clientSocket.recvfrom(2048)


            # self.clientSocket.close()