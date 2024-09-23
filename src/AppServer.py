import ast
import os
import socket
import threading
import time
from server.UDPserver import UDPserver
from server.TCPserver import TCPserver

serverPort = 12000

global masterServer, coms_type, clientsList, clientAddress, portCounter

def clearTerminal():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux or macOS
        os.system('clear')

def waitEntry():
      while True:
            entry = input('Press \'q\' to stop \n\n')
            if entry == 'q':
                  print('finishing run \n')
                  break

def getComsType():
      while True:
            server_type = input('UDP or TCP?\n').strip().lower()
            if server_type in ['udp', 'tcp']:
                  return server_type
            else:
                  print('invalid input\n')

def runServer(server):
      global clientAddress
      running = True
      while running:
            try:
                  clientMessage, clientAddress = server.receiveMessage()
                  handleMessage(clientMessage)
            except socket.timeout:
                  time.sleep(0.1)
            except ConnectionResetError:
                  print(f"Connection reset by client: {clientAddress}\n")
            except Exception as e:
                  print(f"An error occurred: {e}")

def decodeMessage(clientMessage):
      messageReceived = ast.literal_eval(clientMessage.decode())
      sender = messageReceived[0]
      receiver = messageReceived[1]
      operation = messageReceived[2]
      messageContent = messageReceived[3]
      messageType = messageContent[0]
      message = messageContent[1]
      return sender, receiver, operation, messageType, message, clientAddress

def sendMessageToClient(client, clientMessage):
      for clnt in clientsList:
            if clnt[0] == client:
                  clnt[1].sendMessage(clientMessage, clnt[2])

def handleMessage(clientMessage):
      global portCounter
      sender, receiver, operation, messageType, message, clientAddress = decodeMessage(clientMessage)
      if operation == "register":
            for client in clientsList:
                  if client[0] == sender:
                        if client[2] != '':
                              response = "['server','{}','response',['register','already_registered']]".format(sender).encode()
                              sendMessageToClient(client=sender, clientMessage=response)
                              return
                        else:
                              for connection in clientsList:
                                    if connection[3] == sender:
                                          response = "['server','{}','response',['register-connection','{}']]".format(sender, connection[3]).encode()
                                          newServerSocket = None
                                          portCounter = portCounter + 1
                                          if coms_type == 'udp':
                                                newServerSocket = UDPserver(serverPort=portCounter, client=sender)
                                          else:
                                                newServerSocket = TCPserver(serverPort=portCounter, client=sender)
                                          clientsList.append([sender, newServerSocket, clientAddress, ''])
                                          print ("Registered: {}, {}\n".format(sender, str(clientAddress)))
                                          sendMessageToClient(client=sender, clientMessage=response)
                                          return

            response = "['server','{}','response',['register','registered']]".format(sender).encode()

            newServerSocket = None
            portCounter = portCounter + 1
            if coms_type == 'udp':
                  newServerSocket = UDPserver(serverPort=portCounter, client=sender)
            else:
                  newServerSocket = TCPserver(serverPort=portCounter, client=sender)
            clientsList.append([sender, newServerSocket, clientAddress, ''])
            print()
            print ("Registered: {}, {}\n".format(sender, str(clientAddress)))
      elif operation == "new_convo":
            contact_exists = any(message == client[0] for client in clientsList) #confere se contato requerido ja existe
            for c in clientsList:
                  if c[0] == sender:
                        c[3] = message #nome do contato requerido
            if contact_exists:
                  contact = next((client for client in clientsList if client[0] == message), None) #busca contato requerido, caso exista
                  if contact[3] == sender:
                        response = "['{}','{}','response',['new_convo','accepted']]".format(sender, contact[0]).encode()
                        sendMessageToClient(client=contact[0], clientMessage=response)
                        response = "['{}','{}','response',['new_convo','accepted']]".format(contact[0], sender).encode()
                        sendMessageToClient(client=sender, clientMessage=response)
                        print("New convo between {} and {}\n".format(contact[0], sender))
                  elif contact[3] != '':
                        response = "['server','{}','response',['new_convo','denied']]".format(sender).encode()
            else:
                  response = "['server','{}','response',['new_convo','wait']]".format(sender).encode()
                  sendMessageToClient(client=sender, clientMessage=response)
      elif operation == "message":
            contact = next((client for client in clientsList if client[0] == sender), None)
            connection = next(client for client in clientsList if client[0] == contact[3])
            if messageType == "message":
                  serverMessage = "['{}','{}','message',['message','{}']]".format(sender, contact[3], message).encode()
                  sendMessageToClient(client=contact[3], clinetMessage=serverMessage)
      elif operation == "bye_bye":
            contact = next((client for client in clientsList if client[0] == sender), None)
            if contact != None:
                  if contact[3] != "":
                        connection = next(client for client in clientsList if client[0] == contact[3])
                        if connection[3] == contact[0]:
                              connection[3] = ""
                              response = "['server','{}','disconnect',['disconnect','{}']]".format(connection[0], sender).encode()
                              sendMessageToClient(client=connection[0], clientMessage=response)
                  contact = None
                  print ("{} disconnected".format(sender))
      elif operation == "response":
            if messageType == "new_convo":
                  if message == "accepted":
                        contact = next((client for client in clientsList if client[0] == message), None)
                        response = "['{}','{}','response',['new_convo','accepted']]".format(sender, receiver).encode()
                        sendMessageToClient(client=receiver, clientMessage=response)

def start():
      global masterServer, clientsList, coms_type, portCounter
      clientsList = []
      portCounter = 0
      clearTerminal()
      coms_type = getComsType()
      masterServer = None
      clearTerminal()
      if coms_type == 'udp':
            masterServer = UDPserver(serverPort=serverPort, client="master")
            print ('The UDP server is ready to receive')
      else:
            masterServer = TCPserver(serverPort=serverPort, client="master")
            print ('The TCP server is ready to receive')
      serverThread = threading.Thread(target=runServer, args=(masterServer,))
      serverThread.daemon = True
      serverThread.start()
      waitEntry()

start()