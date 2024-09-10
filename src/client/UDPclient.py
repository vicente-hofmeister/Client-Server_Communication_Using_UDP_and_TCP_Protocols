from socket import *

class UDPclient:
      def __init__(self, serverName, serverPort):
            self.serverName = serverName
            self.serverPort = serverPort
            self.clientSocket = socket(AF_INET, SOCK_DGRAM)

      def start(self):
            myName = input('What is your name?')
            friendName = input('Who do you want to talk to?')
            message = input('What do you want to say?')
            messageToServer= "[{},{},{}]".format(myName, friendName, message)

            self.clientSocket.sendto(messageToServer.encode(), (self.serverName, self.serverPort))

            recievedMessage, serverAddress = self.clientSocket.recvfrom(2048)

            print (recievedMessage.decode())

            self.clientSocket.close()