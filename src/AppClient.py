import ast
import os
import sys
import time
from client.UDPclient import UDPclient
from client.TCPclient import TCPclient

serverName = '127.0.0.1'
serverPort = 12000

global myName, connectionName, sender, receiver, operation, messageType, message, serverAddress

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


client = None

clear_terminal()

if get_coms_type() == 'udp':
      client = UDPclient(serverName=serverName, serverPort=serverPort)
else:
      client = TCPclient(serverName=serverName, serverPort=serverPort)

initialize_client()




