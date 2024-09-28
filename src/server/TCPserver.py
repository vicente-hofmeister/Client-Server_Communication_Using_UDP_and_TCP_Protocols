from socket import *

class TCPserver:
      '''
      Makes server socket operations through a TCP connection.

      Attributes:
            serverPort: The port where the server socket runs.
            client: Stores the name of the client utilizing this server socket.
            serverSocket: Socket that listens for incoming connections, then connects the client to the clientSocket.
            clientSocket: Socket used to keep the client connected.
            clientAddress: Address of the connected client.
      
      Methods:
            __init__: Initializes a server socket.
            receiveMessage: Receives a message from the client.
            sendMessage: Sends a message to the client.
            getClient: Returns the name of the connected client.
            closeSocket: Closes this server socket.
      '''
      def __init__(self, serverPort, client):
            '''
            Initializes the server socket with its port and client name.

            The socket has a 0.5-second timeout to allow the same socket to receive and send messages 'simultaneously.'

            Args:
                  serverPort (int): The port number that this server socket uses.
                  client (str): The name of the client connected through this server socket.
            '''
            self.serverPort = serverPort
            self.client = client
            self.serverSocket = socket(AF_INET,SOCK_STREAM)
            self.serverSocket.bind(('',self.serverPort))
            self.serverSocket.settimeout(0.5)
            listenTo = 1
            if client == "master":
                  listenTo = 10
            self.serverSocket.listen(listenTo)
            self.clientSocket = None
            self.clientAddress = None

      def receiveMessage(self):
            '''
            Receives a message from the client. If there is no client connected, waits for a connection.

            Returns:
                  clientMessage (bytes): The encoded message from the client.
                  clientAddress ((str,int)): A tuple containing the client's IPv4 address and port.
            '''
            if self.clientSocket is None:
                  while True:
                        try:
                              self.clientSocket, self.clientAddress = self.serverSocket.accept()
                              break
                        except TimeoutError:
                              pass
                        except OSError as e:
                              print(f"Erro no accept: {e}")
                              break
            try:
                  clientMessage = self.clientSocket.recv(2048)
                  if not clientMessage:
                        self.clientSocket.close()
                        self.clientSocket = None
                        return None, None
                  return clientMessage, self.clientAddress
            except Exception as e:
                  print(f"Erro ao receber mensagem: {e}")
                  return None, None

      def sendMessage(self, message, address):
            '''
            Sends a message to the client.

            Args:
                  message (bytes): The encoded message from the server to the client.
                  address (tuple): A tuple containing the client's IPv4 address (str) and port (int). Not used with a TCP connection, as the client remains connected.
            '''
            if self.clientSocket:
                  try:
                        self.clientSocket.send(message)
                  except Exception as e:
                        print(f"Erro ao enviar mensagem: {e}")
      
      def getClient(self):
            '''
            Gets the client of this server socket.

            Returns:
                  str: The name of the client connected to this server socket.
            '''
            return self.client
      
      def closeSocket(self):
            '''
            Closes the server socket.
            '''
            if self.clientSocket:
                  try:
                        self.clientSocket.close()
                  except Exception as e:
                        print(f"Erro ao fechar clientSocket: {e}")
            try:
                  self.serverSocket.close()  # Fecha o socket do servidor
            except Exception as e:
                  print(f"Erro ao fechar serverSocket: {e}")