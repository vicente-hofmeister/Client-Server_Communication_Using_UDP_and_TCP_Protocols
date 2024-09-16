import ast
import os
import threading
from server.UDPserver import UDPserver
from server.TCPserver import TCPserver

serverPort = 12000

global server, clientsList, sender, receiver, operation, messageType, message, clientAddress
clientsList = []

def clear_terminal():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux or macOS
        os.system('clear')

def wait_entry():
      while True:
            entry = input('Press \'q\' to stop \n')
            if entry == 'q':
                  print('finishing run \n')
                  break

def get_coms_type():
      while True:
            server_type = input('UDP or TCP?\n').strip().lower()
            if server_type in ['udp', 'tcp']:
                  return server_type
            else:
                  print('invalid input\n')

def run_server():
      global clientAddress
      while True:
            clientMessage, clientAddress = server.receiveMessage()
            serverMessage, clientAddress = handleMessage(clientMessage)
            server.sendMessage(serverMessage, clientAddress)

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
            clientsList.append([sender,clientAddress])
            response = "['server','{}','response',['register','registered']]".format(sender)
            print ("Registered: {}, {}".format(sender, str(clientAddress)))
            return (response.encode(), clientAddress)
      elif operation == "new_convo":
            contactName = message
            contact_exists = any(contactName == client[0] for client in clientsList)
            
            if contact_exists:
                  contact = next(client for client in clientsList if client[0] == contactName)
                  response = "['{}','{}','new_convo',['contact','{}']]".format(sender, contact[0], sender)
                  return (response.encode(), contact[1])
            else:
                  response = "['server','{}','response',['new_convo','not_allowed']]".format(sender)
                  return (response.encode(), clientAddress)
      elif operation == "response":
            if messageType == "new_convo":
                  if message == "accepted":
                        contact = next(client for client in clientsList if client[0] == receiver)
                        response = "['{}','{}','response',['new_convo','accepted']]".format(sender, receiver)
                        print("New convo between {} and {}".format(receiver, sender))
                        return (response.encode(), contact[1])

def start():
      global server
      clear_terminal()
      coms_type = get_coms_type()
      server = None
      clear_terminal()
      if coms_type == 'udp':
            server = UDPserver(serverPort=serverPort)
      else:
            server = TCPserver(serverPort=serverPort)
      serverThread = threading.Thread(target=run_server)
      serverThread.daemon = True
      serverThread.start()
      wait_entry()

start()