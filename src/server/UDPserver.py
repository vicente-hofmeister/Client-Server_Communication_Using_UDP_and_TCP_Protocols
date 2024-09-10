from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ('The server is ready to receive')
while True:
      messageFromClient1, client1Address = serverSocket.recvfrom(2048)
      messageFromClient2, client2Address = serverSocket.recvfrom(2048)

      serverSocket.sendto(messageFromClient2,client1Address)
      serverSocket.sendto(messageFromClient1,client2Address)