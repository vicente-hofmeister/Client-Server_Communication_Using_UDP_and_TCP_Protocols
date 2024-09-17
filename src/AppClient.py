import ast
import os
import sys
import threading
import time
from client.UDPclient import UDPclient
from client.TCPclient import TCPclient

serverName = '127.0.0.1'
serverPort = 12000
serverAddress = (serverName, serverPort)

global client, myName, connectionName, connected, sender, receiver, operation, messageType, message, stop_event 

def clear_terminal():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux or macOS
        os.system('clear')

def my_screen():
      clear_terminal()
      print("{}'s chat:".format(myName))

def get_coms_type():
      while True:
            server_type = input('UDP or TCP?\n').strip().lower()
            if server_type in ['udp', 'tcp']:
                  return server_type
            else:
                  print('invalid input')

def initialize_client() :
      global myName
      clear_terminal()
      myName = input('What is your name?\n')
      client.sendMessage(message="['{}','server','register',['','']]".format(myName).encode())
      serverMessage = client.receiveMessage()
      manage_response(serverMessage)


     
def decode_message(receivedMessage):
      global sender, receiver, operation, messageType, message, serverAddress
      messageReceived = ast.literal_eval(receivedMessage[0].decode())
      sender = messageReceived[0]
      receiver = messageReceived[1]
      operation = messageReceived[2]
      messageContent = messageReceived[3]
      messageType = messageContent[0]
      message = messageContent[1]
      serverAddress = receivedMessage[1]

def manage_response(receivedMessage):
      global connected
      decode_message(receivedMessage)
      if operation == "response":
            if messageType == "register":
                  if message == "registered":
                        clear_terminal()
                        print("Registered!\n")
                        time.sleep(2)
                        my_screen()
                  elif message == "already_registered":
                        print("Name already registered. Please, enter another name.")
                        time.sleep(3)
                        initialize_client()
            elif messageType == "register-connection":                  
                  answer = input("{} wants to connect! Do you accept? (y or n)".format(message))
                  while answer.lower() != "y" and answer.lower() != "n":
                        print("invalid answer.")
                        answer = input("{} wants to connect! Do you accept? (y or n)".format(message))
                  if answer == "n":
                        print("Too bad...\n")
                  my_screen()
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
                        manage_response(client.receiveMessage())  
                        # elif clientChoice == "c":
                        #       connect()
                        # else:
                        #       closeConnection()
                        #       sys.exit(0)
                  elif message == "accepted":
                        my_screen()
                        print("Connected!")
                        connected = True
                  elif message == "denied":
                        print("Contact denied the connection :(")
                        time.sleep(3)
                        my_screen()
                        connect()
      elif operation == "new_convo":
            if messageType == "contact":
                  clear_terminal()
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
            my_screen()
            print ("The name can not be empty")
            friendName = input("Who do you wish to connect with? Write their name!\n")

      connectionName = friendName
      my_screen()
      print("Waiting connection with {}...".format(connectionName))

      clientMessage = "['{}','server','new_convo',['contact','{}']]".format(myName, connectionName).encode()
      client.sendMessage(clientMessage)
      manage_response(client.receiveMessage())
      
def waitMessage():
      while not stop_event.is_set():
            receivedMessage = client.receiveMessage()
            stop_event.set()
            newMessage = manage_response(receivedMessage)
            client.sendMessage(newMessage)
            stop_event.clear()

def closeConnection():
      #byebye message to server
      client.closeConnection()

def start():
      global client, stop_event, connected
      client = None
      connected = False
      stop_event = threading.Event()
      clear_terminal()

      if get_coms_type() == 'udp':
            client = UDPclient(serverAddress=serverAddress)
      else:
            client = TCPclient(serverAddress=serverAddress)

      initialize_client()
      connect()

      # sendConnectThread = threading.Thread(target=sendConnect)
      waitMessageThread = threading.Thread(target=waitMessage)
      # sendMessageThread = threading.Thread(target=sendMessage)

      # sendConnectThread.start()
      # waitMessageThread.start()

      # byebye message here
      closeConnection()

start()