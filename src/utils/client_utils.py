import ast
import os
import time

global myName, connectionName, sender, receiver, operation, messageType, message, serverAddress

def __init__(self):
      return

def clear_terminal():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux or macOS
        os.system('clear')

def initialize_client() :
      global myName
      clear_terminal()
      myName = input('What is your name?\n')
      return "['{}','server','register',['','']]".format(myName).encode()

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

def check_register(receivedMessage):
      decode_message(receivedMessage)

      if message == 'registered':
            clear_terminal()
            print("Registered!\n")
            time.sleep(2)
            clear_terminal()
            print("{}'s chat:".format(myName))
            return True
      
      return False

def manage_response(receivedMessage):
      decode_message(receivedMessage)

      if operation == "response":
            originalOperation = messageType
            response = message

            if originalOperation == "new_convo" and response == "not_allowed":
                  print("There is no contact with that name :(\n")
                  return "denied"

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

def choose_friend():
      print("Wish to connect with someone? Write their name!\n")
      friendName = input()
      print("Trying to connect...")
      return ("['{}','server','new_convo',['contact','{}']]".format(myName, friendName).encode(), serverAddress)
