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

global client, myName, connectionName, sender, receiver, operation, messageType, message, stop_event 

def clear_terminal():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux or macOS
        os.system('clear')


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

      decode_message(serverMessage)
      
      if message == 'registered':
            clear_terminal()
            print("Registered!\n")
            time.sleep(2)
            clear_terminal()
            print("{}'s chat:".format(myName))
      else:
            client.closeConnection()
            sys.exit(1)
     
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
      decode_message(receivedMessage)

      if operation == "response":
            if messageType == "new_convo" and message == "not_allowed":
                  print("There is no contact with that name :(\n")
                  return "denied"
            elif messageType == "new_convo" and message == "accepted":
                  print("Connected!")
                  return "accepted"
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

def getFromKeyboard():
      answer = ""

      def get_input():
            answer = input()

      input_thread = threading.Thread(target=get_input)
      input_thread.start()
      input_thread.join()
      while not stop_event.is_set():
            answer = input()
            stop_event.set

      return answer


def sendConnect():
      global stop_event
      response = ""
      while not stop_event.is_set():
            print("Wish to connect with someone? Write their name!\n")
            friendName = getFromKeyboard()
            if friendName != "":
                  stop_event.set()
                  print("Trying to connect...")
                  clientMessage = "['{}','server','new_convo',['contact','{}']]".format(myName, friendName).encode()
                  client.sendMessage(clientMessage)
                  response = manage_response(client.receiveMessage())

                  if type(response) == "str" and response == "denied":
                        stop_event.clear()

def waitMessage():
      while not stop_event.is_set():
            receivedMessage = client.receiveMessage()
            stop_event.set()
            newMessage = manage_response(receivedMessage)
            client.sendMessage(newMessage)
            stop_event.clear()

def start():
      global client, stop_event
      client = None
      stop_event = threading.Event()
      clear_terminal()

      if get_coms_type() == 'udp':
            client = UDPclient(serverAddress=serverAddress)
      else:
            client = TCPclient(serverAddress=serverAddress)

      initialize_client()

      sendConnectThread = threading.Thread(target=sendConnect)
      waitMessageThread = threading.Thread(target=waitMessage)
      # sendMessageThread = threading.Thread(target=sendMessage)

      sendConnectThread.start()
      waitMessageThread.start()

      # byebye message here
      # client.closeConnection()

start()