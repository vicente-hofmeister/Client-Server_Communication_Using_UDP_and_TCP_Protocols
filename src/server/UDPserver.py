from socket import *

class UDPserver:
      '''
      Performs server socket operations through a UDP connection.

      Attributes:
            serverPort: The port where the server socket runs.
            client: Stores the name of the client utilizing this server socket.
            serverSocket: Socket that listens for incoming messages from the client.
            
      Methods:
            __init__: Initializes the server socket.
            receiveMessage: Receives a message from the client.
            sendMessage: Sends a message to the client.
            getClient: Returns the name of the connected client.
            closeSocket: Closes the server socket.
      '''
      def __init__(self, serverPort, client):
            '''
            Initializes the server socket with its port and client name.

            Args:
                  serverPort (int): The port number that this server socket uses.
                  client (str): The name of the client connected through this server socket.
            '''    
            self.serverPort = serverPort
            self.serverSocket = socket(AF_INET, SOCK_DGRAM)
            self.serverSocket.bind(('', self.serverPort))
            self.serverSocket.settimeout(0.1)
            self.client = client

      def receiveMessage(self):
            '''
            
            Receives a message from the client. If there is not a client connected, waits to connect.

            Returns:
                  bytes: Encoded client message

            '''
            clientMessage =  self.serverSocket.recvfrom(2048)
            return clientMessage
      
      def sendMessage(self, message, address):
            '''
            Receives a message from the client. If there is no client connected, waits for a connection.

            Returns:
                  bytes: The encoded message from the client.
            '''


            self.serverSocket.sendto(message, address)

      def getClient(self):
            '''
            Gets the client of this server socket.

            Returns:
                  str: The name of the client connected to this server socket.
            '''
            return self.client
      
      def closeSocket(self):
            '''
            Closes this server socket.
            '''
            self.serverSocket.close()