from socket import *
serverName = '127.0.0.1' #endereco ipv4. localhost = 127.0.0.1
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

myName = input('What is your name?')
friendName = input('Who do you want to talk to?')
message = input('What do you want to say?')
messageToServer= "[{},{},{}]".format(myName, friendName, message)

clientSocket.sendto(messageToServer.encode(), (serverName, serverPort))

recievedMessage, serverAddress = clientSocket.recvfrom(2048)

print (recievedMessage.decode())



clientSocket.close()
