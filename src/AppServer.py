import ast
import os
import threading
from server.UDPserver import UDPserver
from server.TCPserver import TCPserver

serverPort = 12000

global server, clientsList, sender, receiver, operation, messageType, message, clientAddress

def clearTerminal():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux or macOS
        os.system('clear')

def waitEntry():
      while True:
            entry = input('Press \'q\' to stop \n')
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

def runServer():
    global clientAddress
    while True:
        try:
            clientMessage, clientAddress = server.receiveMessage()
            handleMessage(clientMessage)
        except ConnectionResetError:
            print(f"Connection reset by client: {clientAddress}\n")
        except Exception as e:
            print(f"An error occurred: {e}")

def decodeMessage(clientMessage):
      global sender, receiver, operation, messageType, message, clientAddress
      messageReceived = ast.literal_eval(clientMessage.decode())
      sender = messageReceived[0]
      receiver = messageReceived[1]
      operation = messageReceived[2]
      messageContent = messageReceived[3]
      messageType = messageContent[0]
      message = messageContent[1]

def handleMessage(clientMessage):
      decodeMessage(clientMessage)
      if operation == "register":
            for client in clientsList:
                  if client[0] == sender:
                        if client[1] != '':
                              response = "['server','{}','response',['register','already_registered']]".format(sender).encode()
                              server.sendMessage(message=response, address=clientAddress)
                              return
                        else:
                              for connection in clientsList:
                                    if connection[2] == sender:
                                          response = "['server','{}','response',['register-connection','{}']]".format(sender, connection[2]).encode()
                                          clientsList.append([sender,clientAddress, ''])
                                          print ("Registered: {}, {}\n".format(sender, str(clientAddress)))
                                          server.sendMessage(message=response, address=clientAddress)
                                          return

            response = "['server','{}','response',['register','registered']]".format(sender).encode()
            server.sendMessage(message=response, address=clientAddress)
            
            clientsList.append([sender,clientAddress, ''])
            print ("Registered: {}, {}\n".format(sender, str(clientAddress)))
      elif operation == "new_convo":
            contact_exists = any(message == client[0] for client in clientsList) #confere se contato requerido ja existe
            for c in clientsList:
                  if c[0] == sender:
                        c[2] = message #nome do contato requerido
            if contact_exists:
                  contact = next((client for client in clientsList if client[0] == message), None) #busca contato requerido, caso exista
                  if contact[2] == sender:
                        response = "['{}','{}','response',['new_convo','accepted']]".format(sender, contact[0]).encode()
                        server.sendMessage(message=response, address=contact[1])
                        response = "['{}','{}','response',['new_convo','accepted']]".format(contact[0], sender).encode()
                        server.sendMessage(message=response, address=clientAddress)
                        print("New convo between {} and {}\n".format(contact[0], sender))
                  elif contact[2] != '':
                        response = "['server','{}','response',['new_convo','denied']]".format(sender).encode()
            else:
                  response = "['server','{}','response',['new_convo','wait']]".format(sender).encode()
                  server.sendMessage(message=response, address=clientAddress)
      elif operation == "message":
            contact = next((client for client in clientsList if client[0] == sender), None)
            connection = next(client for client in clientsList if client[0] == contact[2])
            if messageType == "message":
                  serverMessage = "['{}','{}','message',['message','{}']]".format(sender, contact[2], message).encode()
                  server.sendMessage(serverMessage, connection[1])
      elif operation == "bye_bye":
            contact = next((client for client in clientsList if client[0] == sender), None)
            if contact != None:
                  if contact[2] != "":
                        connection = next(client for client in clientsList if client[0] == contact[2])
                        if connection[2] == contact[0]:
                              connection[2] = ""
                              response = "['server','{}','disconnect',['disconnect','{}']]".format(connection[0], sender).encode()
                              server.sendMessage(response, connection[1])
                  contact = None
                  print ("{} disconnected".format(sender))
      elif operation == "response":
            if messageType == "new_convo":
                  if message == "accepted":
                        contact = next((client for client in clientsList if client[0] == message), None)
                        response = "['{}','{}','response',['new_convo','accepted']]".format(sender, receiver).encode()
                        server.sendMessage(message=response, address=contact[1])

def start():
      global server, clientsList
      clientsList = []
      clearTerminal()
      coms_type = getComsType()
      server = None
      clearTerminal()
      if coms_type == 'udp':
            server = UDPserver(serverPort=serverPort)
      else:
            server = TCPserver(serverPort=serverPort)
      serverThread = threading.Thread(target=runServer)
      serverThread.daemon = True
      serverThread.start()
      waitEntry()

start()