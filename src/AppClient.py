import ast
import os
import socket
import sys
import threading
import time
import colorama
from colorama import Fore, Style
from client.UDPclient import UDPclient
from client.TCPclient import TCPclient

global client, myName, connectionName, connected, stop_event, messagesList, serverAddress, messageId

serverName = '127.0.0.1'
serverPort = 12000
serverAddress = (serverName, serverPort)
colorama.init(autoreset=True)
LIGHT_BLUE = '\033[94m'
YELLOW = '\033[93m'

def clearTerminal():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux or macOS
        os.system('clear')

def printMessages():
    for msg in messagesList:
        printedMessage = ""
        if msg[0] == myName:
            printedMessage = f"{YELLOW}{msg[0]}:{Style.RESET_ALL}"
        else:
            printedMessage = f"{LIGHT_BLUE}{msg[0]}:{Style.RESET_ALL}"

        if msg[2] == "message":
            printedMessage += f"  {msg[3]}"
        
        print(printedMessage)

def myScreen(complete):
    clearTerminal()
    print(f"{YELLOW}{myName}'s chat:{Style.RESET_ALL}")
    print(f"{YELLOW}Talking to {serverAddress}{Style.RESET_ALL}")

    if complete:
        printMessages()
        print(f"{YELLOW}Type a new message to send: (--help to see the commands){Style.RESET_ALL}")

def createDirectories():
    directories = ['downloaded_files', 'files_to_send']

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Diretório '{directory}' criado.")
        else:
            print(f"Diretório '{directory}' já existe.")

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
      myName = input('What is your name?\n').strip()
      client.sendMessage(message="['{}','server','register',['','']]".format(myName).encode('utf-8'))
      serverMessage = receiveSingleMessage()
      manageResponse(serverMessage)

def decodeMessage(serverMessage):
      global serverAddress
      
      messageReceived = ast.literal_eval(serverMessage[0].decode('utf-8'))
      sender = messageReceived[0]
      receiver = messageReceived[1]
      operation = messageReceived[2]
      messageContent = messageReceived[3]
      messageType = messageContent[0]
      message = []
      for i in range(1,len(messageContent)):
            message.append(messageContent[i])
      
      # if serverAddress != serverMessage[1]:
      #       serverAddress = serverMessage[1]
      #       client.changeServerAddress(newAddress=serverAddress)
      return sender, receiver, operation, messageType, message

def manageResponse(serverMessage):
      global connected, messagesList, serverAddress
      sender, receiver, operation, messageType, message= decodeMessage(serverMessage)
      if operation == "response":
            if messageType == "register":
                  if message[0] == "registered":
                        serverAddress = (serverName, int(message[1]))
                        client.changeServerAddress(serverAddress)
                        clearTerminal()
                        print("Registered!\n")
                        time.sleep(2)
                        myScreen(False)
                  elif message[0] == "already_registered":
                        print("Name already registered. Please, enter another name.")
                        time.sleep(3)
                        initializeClient()
            elif messageType == "register-connection":                  
                  answer = input("{} wants to connect! Do you accept? (y or n)".format(message[0]))
                  while answer.lower() != "y" and answer.lower() != "n":
                        print("invalid answer.")
                        answer = input("{} wants to connect! Do you accept? (y or n)".format(message[0]))
                  if answer == "n":
                        print("Too bad...\n")
                  myScreen(False)
                  print("Connected!")
                  messagesList = []
                  connected = True
                  clientMessage = "['{}','{}','response',['new_convo','accepted']]".format(myName, message[0]).encode('utf-8')
                  client.sendMessage(clientMessage)
            elif messageType == "new_convo":
                  if message[0] == "wait":
                        # print("There is no current contact with this name.\n")
                        # clientChoice = input("Do you wish to: wait(w), make new connection(c) or to quit(q)?")
                        # while clientChoice != "w" and clientChoice != "c" and clientChoice != "q":
                        #       print("Please, make a valid choice.")
                        #       clientChoice = input("Do you wish to: wait(w), make new connection(c) or to quit(q)?")
                        # if clientChoice == "w":
                        #       clientMessage = "['{}','server','response',['wait','ok']]".format(myName).encode('utf-8')
                        serverMessage = receiveSingleMessage()
                        manageResponse(serverMessage)  
                        # elif clientChoice == "c":
                        #       connect()
                        # else:
                        #       closeConnection()
                        #       sys.exit(0)
                  elif message[0] == "accepted":
                        myScreen(False)
                        print("Connected!")
                        time.sleep(3)
                        messagesList = []
                        connected = True
                  elif message[0] == "denied":
                        print("Contact denied the connection :(")
                        time.sleep(3)
                        myScreen(False)
                        connect()
      elif operation == "new_convo":
            if messageType == "contact":
                  clearTerminal()
                  print("{} wants to begin a new contact with you!".format(str(message[0]).capitalize()))
                  answer = ""
                  while answer.lower() != 'n' and answer.lower() != 'y':
                        answer = input("Do you want to connect? (y or n)\n")
                  if answer.lower() == 'n':
                        client.sendMessage("['{}','{}','response',['new_convo','denied']]".format(myName, sender).encode('utf-8'), serverAddress)
                  else:
                        client.sendMessage("['{}','{}','response',['new_convo','accepted']]".format(myName, sender).encode('utf-8'), serverAddress)
      elif operation == "message":
            messagesList.append([connectionName, message[0], messageType, message[1]])
            if message[0] == len(messagesList):
                  print("\033[91mWe probably lost some message(s) along the way\033[0m")
            myScreen(True)

def connect():
      global connectionName
      friendName = input("Who do you wish to connect with? Write their name!\n")
      
      while friendName == "":
            myScreen(False)
            print ("The name can not be empty")
            friendName = input("Who do you wish to connect with? Write their name!\n")

      connectionName = friendName
      myScreen(False)
      print("Waiting connection with {}...".format(connectionName))

      clientMessage = "['{}','server','new_convo',['contact','{}']]".format(myName, connectionName).encode('utf-8')
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

def uploadFile():
      global messageId, messagesList
      directory = 'files_to_send'
      files = os.listdir(directory)
      
      if files:
            print("Choose a file: (--cancel to abort the operation)")
            for file in files:
                  print(f"- {file}")

            selection = input()

            if selection == "--cancel":
                  myScreen(True)
                  return
            
            while not selection in files or selection == "--cancel":
                  if selection == "--cancel":
                        myScreen(True)
                        return
                  selection = input("please, choose a valid file\n")
            
            messageId += 1
            file_path = os.path.join(directory, selection)

            with open(file_path, 'rb') as file:
                  file.seek(0, os.SEEK_END)
                  file_size = file.tell()
                  print("file size: {}".format(file_size))
                  file.seek(0)
                  total_readed = 0
                  more_chunks = 1

                  while chunk := file.read(1024):
                        offset = total_readed
                        total_readed += len(chunk)
                        if total_readed == file_size:
                              more_chunks = 0
                        # sends [sender, receiver, opetation(message), [messageType(file), messageId, more_chunks, offset, chunk]]
                        clientMessage = "['{}','{}','message',['file','{}','{}',{},'{}',{}]]".format(myName,connectionName,messageId,selection,more_chunks,offset,chunk).encode('utf-8')

                        client.sendMessage(clientMessage)
      else:
            print("There are no files in 'files_to_send'")

def waitEntry():
      global messagesList, messageId
      while True:
            entry = input()
            if entry == "--exit":
                  print("finishing run\n")
                  stop_event.set()
                  break
            elif entry == "--upload":
                  uploadFile()
            elif entry == "--download":
                  None
            elif entry == "--help":
                  myScreen(True)
                  print("App client commands:\n\t'--upload' to choose a file from the 'files_to_send' folder to send to your contact\n\t'--download' to choose a file that your contact has sent to you to download to 'downloaded_files'\n\t'--exit' to quit the application")
            else:
                  messageId += 1
                  clientMessage = "['{}','{}','message',['message','{}','{}']]".format(myName, connectionName, messageId, entry).encode('utf-8')
                  client.sendMessage(clientMessage)
                  messagesList.append([myName, messageId,"message",entry])
                  myScreen(True)
      
def closeConnection():
      clientMessage = "['{}','server','bye_bye',['','']]".format(myName).encode('utf-8')
      client.sendMessage(clientMessage)
      client.closeConnection()

def start():
      global client, stop_event, connected, messageId
      createDirectories()
      client = None
      connected = False
      messageId = 0
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
      myScreen(True)
      waitEntry()

      waitMessageThread.join()
      closeConnection()

start()