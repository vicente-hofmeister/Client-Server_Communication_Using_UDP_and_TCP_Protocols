from socket import *
class UDPclient:
      '''
      Performs client socket operations through a UDP connection.

      Attributes:
            serverAddress: A tuple (str, int) representing the IPv4 address and the port of the server.
            clientSocket: The socket responsible for the client's UDP communications.

      Methods:
            __init__: Initializes the client's socket.
            changeServerAddress: Changes the server socket address with which the client communicates.
            sendMessage: Sends an encoded message from the client to the server.
            receiveMessage: Receives an encoded message from the server to the client.
            closeConnection: Closes the client socket.
      '''
      def __init__(self, serverAddress):
            '''
            Initializes the client socket to communicate with the given server address.

            Args:
                  serverAddress ((str, int)): A tuple with the ipv4 address and port for the initial server socket
            '''
            self.serverAddress = serverAddress
            self.clientSocket = socket(AF_INET, SOCK_DGRAM)
            self.clientSocket.settimeout(0.5)

      def changeServerAddress(self, newAddress):
            '''
            Changes the server socket address to communicate with the socket dedicated to this client.

            Args:
                  newAddress ((str, int)): A tuple containing the IPv4 address and port of the server socket.
            '''
            self.serverAddress = newAddress

      def sendMessage(self, message):
            '''
            Sends an encoded message from the client to the server.

            Args:
                  message (bytes): The encoded message to be sent from the client.
            '''
            self.clientSocket.sendto(message, self.serverAddress)

      def receiveMessage(self):
            '''
            Receives an encoded message from the server.

            Returns:
                  serverMessage (bytes): The encoded message from the server.
                  serverAddress (tuple): A tuple (str, int) containing the IPv4 address and port of the server socket.
            '''
            serverMessage = self.clientSocket.recvfrom(2048)
            return serverMessage

      def closeConnection(self):
            '''
            Closes the current socket.
            '''
            self.clientSocket.close()