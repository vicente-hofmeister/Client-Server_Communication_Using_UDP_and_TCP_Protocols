from socket import *

class TCPserver:
      def __init__(self, serverPort, client):
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
            if self.clientSocket:
                  try:
                        self.clientSocket.send(message)
                  except Exception as e:
                        print(f"Erro ao enviar mensagem: {e}")
      
      def getClient(self):
            return self.client
      
      def closeSocket(self):
            if self.clientSocket:
                  try:
                        self.clientSocket.close()
                  except Exception as e:
                        print(f"Erro ao fechar clientSocket: {e}")
            try:
                  self.serverSocket.close()  # Fecha o socket do servidor
            except Exception as e:
                  print(f"Erro ao fechar serverSocket: {e}")