from socket import *
class TCPclient:
      '''
      Performs client socket operations through a TCP connection.

      Attributes:
            serverAddress: A tuple (str, int) representing the IPv4 address and the port of the server.
            clientSocket: The socket responsible for the client's TCP communications.

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
            self.clientSocket = socket(AF_INET, SOCK_STREAM)
            self.clientSocket.settimeout(0.1)
            self.clientSocket.connect(self.serverAddress)

      def changeServerAddress(self, newAddress):
            '''
            Changes the server socket address to communicate with the socket dedicated to this client.

            Args:
                  newAddress ((str, int)): A tuple containing the IPv4 address and port of the server socket.
            '''
            self.serverAddress = newAddress
            self.clientSocket.close()
            self.clientSocket = socket(AF_INET, SOCK_STREAM)
            self.clientSocket.settimeout(0.5)
            self.clientSocket.connect(self.serverAddress)

      def sendMessage(self, message):
            '''
            Sends an encoded message from the client to the server.

            Args:
                  message (bytes): The encoded message to be sent from the client.
            '''
            self.clientSocket.send(message)
      
      def receiveMessage(self):
            '''
            Receives an encoded message from the server.

            Returns:
                  serverMessage (bytes): The encoded message from the server.
                  serverAddress (tuple): A tuple (str, int) containing the IPv4 address and port of the server socket.
            '''
            serverMessage = self.clientSocket.recv(2048)
            return serverMessage, self.serverAddress
      
      def closeConnection(self):
            '''
            Closes the current socket.
            '''
            self.clientSocket.close()
