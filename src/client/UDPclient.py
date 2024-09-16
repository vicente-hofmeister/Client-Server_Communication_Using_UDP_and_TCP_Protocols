import ast
from socket import *
import threading

from utils import client_utils as utils

class UDPclient:
      def __init__(self, serverName, serverPort):
            self.serverAddress = (serverName, serverPort)
            self.clientSocket = socket(AF_INET, SOCK_DGRAM)
            self.stop_event = threading.Event()

      def start(self):
            
            def sendConnect():
                  while not self.stop_event.is_set():
                        clientMessage, serverAddress = utils.choose_friend()
                        self.stop_event.set()
                        self.clientSocket.sendto(clientMessage, serverAddress)
                        response = utils.manage_response(self.clientSocket.recvfrom(2048))

                        if type(response) == "str" and response == "accepted":
                              return
            
            def waitMessage():
                  while not self.stop_event.is_set():
                        receivedMessage = self.clientSocket.recvfrom(2048)
                        self.stop_event.set()
                        utils.manage_response(receivedMessage)

            sendConnectThread = threading.Thread(target=sendConnect)
            receiveConnectThread = threading.Thread(target= waitMessage)

            sendConnectThread.start()
            receiveConnectThread.start()

      def sendMessage(self, message):
            self.clientSocket.sendto(message, self.serverAddress)

      def receiveMessage(self):
            serverMessage = self.clientSocket.recvfrom(2048)
            return serverMessage


      def closeConnection(self):
            self.clientSocket.close()