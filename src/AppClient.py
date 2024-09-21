import ast
import os
import socket
import sys
import threading
import time
from client.UDPclient import UDPclient
from client.TCPclient import TCPclient

serverName = '127.0.0.1'
serverPort = 12000
serverAddress = (serverName, serverPort)

global client, myName, connectionName, connected, sender, receiver, operation, messageType, message, stop_event 

def clearTerminal():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux or macOS
        os.system('clear')

def myScreen():
      clearTerminal()
      print("{}'s chat:".format(myName))

def getComsType():
      while True:
            server_type = input('UDP or TCP?\n').strip().lower()
            if server_type in ['udp', 'tcp']:
                  return server_type
            else:
                  print('invalid input')

def initializeClient() :
      global myName
      clearTerminal()
      myName = input('What is your name?\n')
      client.sendMessage(message="['{}','server','register',['','']]".format(myName).encode())
      serverMessage = receiveSingleMessage()
      manageResponse(serverMessage)

def decodeMessage(serverMessage):
      global sender, receiver, operation, messageType, message, serverAddress
      messageReceived = ast.literal_eval(serverMessage[0].decode())
      sender = messageReceived[0]
      receiver = messageReceived[1]
      operation = messageReceived[2]
      messageContent = messageReceived[3]
      messageType = messageContent[0]
      message = messageContent[1]
      serverAddress = serverMessage[1]

def manageResponse(serverMessage):
      global connected
      decodeMessage(serverMessage)
      if operation == "response":
            if messageType == "register":
                  if message == "registered":
                        clearTerminal()
                        print("Registered!\n")
                        time.sleep(2)
                        myScreen()
                  elif message == "already_registered":
                        print("Name already registered. Please, enter another name.")
                        time.sleep(3)
                        initializeClient()
            elif messageType == "register-connection":                  
                  answer = input("{} wants to connect! Do you accept? (y or n)".format(message))
                  while answer.lower() != "y" and answer.lower() != "n":
                        print("invalid answer.")
                        answer = input("{} wants to connect! Do you accept? (y or n)".format(message))
                  if answer == "n":
                        print("Too bad...\n")
                  myScreen()
                  print("Connected!")
                  connected = True
                  clientMessage = "['{}','{}','response',['new_convo','accepted']]".format(myName, message).encode()
                  client.sendMessage(clientMessage)
            elif messageType == "new_convo":
                  if message == "wait":
                        # print("There is no current contact with this name.\n")
                        # clientChoice = input("Do you wish to: wait(w), make new connection(c) or to quit(q)?")
                        # while clientChoice != "w" and clientChoice != "c" and clientChoice != "q":
                        #       print("Please, make a valid choice.")
                        #       clientChoice = input("Do you wish to: wait(w), make new connection(c) or to quit(q)?")
                        # if clientChoice == "w":
                        #       clientMessage = "['{}','server','response',['wait','ok']]".format(myName).encode()
                        serverMessage = receiveSingleMessage()
                        manageResponse(serverMessage)  
                        # elif clientChoice == "c":
                        #       connect()
                        # else:
                        #       closeConnection()
                        #       sys.exit(0)
                  elif message == "accepted":
                        myScreen()
                        print("Connected!")
                        connected = True
                  elif message == "denied":
                        print("Contact denied the connection :(")
                        time.sleep(3)
                        myScreen()
                        connect()
      elif operation == "new_convo":
            if messageType == "contact":
                  clearTerminal()
                  print("{} wants to begin a new contact with you!".format(str(message).capitalize()))
                  answer = ""
                  while answer.lower() != 'n' and answer.lower() != 'y':
                        answer = input("Do you want to connect? (y or n)\n")
                  if answer.lower() == 'n':
                        return ("['{}','{}','response',['new_convo','denied']]".format(myName, sender).encode(), serverAddress)
                  else:
                        return ("['{}','{}','response',['new_convo','accepted']]".format(myName, sender).encode(), serverAddress)

def connect():
      global connectionName
      friendName = input("Who do you wish to connect with? Write their name!\n")
      
      while friendName == "":
            myScreen()
            print ("The name can not be empty")
            friendName = input("Who do you wish to connect with? Write their name!\n")

      connectionName = friendName
      myScreen()
      print("Waiting connection with {}...".format(connectionName))

      clientMessage = "['{}','server','new_convo',['contact','{}']]".format(myName, connectionName).encode()
      client.sendMessage(clientMessage)
      serverMessage = receiveSingleMessage()
      manageResponse(serverMessage=serverMessage)

def receiveSingleMessage():
      running = True
      while running:
            try:
                  serverMessage = client.receiveMessage()
                  return serverMessage
            except socket.timeout:
                  time.sleep(0.1) 
            except Exception as e:
                  print("Error: {}".format(e))
                  running = False

def waitMessage():
      running = True
      while running:
            if stop_event.is_set():
                  running = False
            else:
                  try:
                        serverMessage = client.receiveMessage()
                        manageResponse(serverMessage=serverMessage)
                  except socket.timeout:
                        time.sleep(0.1)
                  except Exception as e:
                        print("Error: {}".format(e))
                        running = False

def waitEntry():
      while True:
            entry = input("Want to sendo a message? (type --exit to quit)\n")
            if entry == "--exit":
                  print("finishing run\n")
                  stop_event.set()
                  break
            else:
                  clientMessage = "['{}','server','message',['message','{}']]".format(myName, entry).encode()
                  client.sendMessage(clientMessage)
      

def closeConnection():
      #byebye message to server
      clientMessage = "['{}','server','bye_bye',['','']]".format(myName).encode()
      client.sendMessage(clientMessage)

      client.closeConnection()

def start():
      global client, stop_event, connected
      client = None
      connected = False
      stop_event = threading.Event()
      clearTerminal()

      if getComsType() == 'udp':
            client = UDPclient(serverAddress=serverAddress)
      else:
            client = TCPclient(serverAddress=serverAddress)

      initializeClient()
      connect()

      waitMessageThread = threading.Thread(target=waitMessage)

      waitMessageThread.start()
      waitEntry()
      # byebye message here
      closeConnection()

start()