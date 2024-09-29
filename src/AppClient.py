import ast
import os
import socket
import threading
import time
import colorama
from colorama import Fore, Style
from client.UDPclient import UDPclient
from client.TCPclient import TCPclient

global client, myName, connectionName, connected, stop_event, messagesList, serverAddress, messageId, filesList

serverName = '127.0.0.1'
serverPort = 12000
serverAddress = (serverName, serverPort)
colorama.init(autoreset=True)
LIGHT_BLUE = '\033[94m'
YELLOW = '\033[93m'
LIGHT_GRAY = '\033[90m'
LIGHT_RED = '\033[91m'
LIGHT_GREEN = '\033[92m'

def clearTerminal():
      '''
      Cleans the terminal to display only the server information.

      Checks the OS to execute the correct command.
      '''
      if os.name == 'nt':  # Windows
            os.system('cls')
      else:  # Linux or macOS
            os.system('clear')

def printMessages():
      '''
      Prints the messages on the terminal. Uses colorama to manage colors.
      '''
      for msg in messagesList:
            printedMessage = ""
            if msg[0] == myName:
                  printedMessage = f"{YELLOW}{msg[0]}:{Style.RESET_ALL}"
            else:
                  printedMessage = f"{LIGHT_BLUE}{msg[0]}:{Style.RESET_ALL}"

            if msg[2] == "message":
                  printedMessage += f"  {msg[3]}"
            elif msg[2] == "file":
                  if msg[4] == "sent":
                        printedMessage += f"  {LIGHT_GRAY}[{msg[3].upper()}]"
                  elif msg[4] == "received":
                        printedMessage += f"  {LIGHT_GREEN}[{msg[3].upper()}]"
                  elif msg[4] == "error":
                        printedMessage += f"  {LIGHT_RED}[{msg[3].upper()}]"
                  elif msg[4] == "not-downloaded":
                        printedMessage += f"  {LIGHT_GRAY}[{msg[3].upper()}]"
                  elif msg[4] == "downloaded":
                        printedMessage += f"  {LIGHT_GREEN}[{msg[3].upper()}]"

            print(printedMessage)

def myScreen(complete):
      '''
      Prints the client screen on the terminal. If the client is connected with another, uses 'complete' to show messages.

      Args:
            complete (bool): True if the messages are shown, False otherwise.
      '''
      clearTerminal()
      print(f"{YELLOW}{myName}'s chat:{Style.RESET_ALL}")
      print(f"{YELLOW}Talking to {serverAddress}{Style.RESET_ALL}")

      if complete:
            printMessages()
            print(f"{YELLOW}Type a new message to send: (--help to see the commands){Style.RESET_ALL}")

def createDirectories():
      '''
      Creates the 'download_files' and 'files_to_send' directories if they don't already exist.
      '''
      directories = ['downloaded_files', 'files_to_send']

      for directory in directories:
            if not os.path.exists(directory):
                  os.makedirs(directory)
                  print(f"Diretório '{directory}' criado.")
            else:
                  print(f"Diretório '{directory}' já existe.")

def saveFiles(fileData, fileName):
      '''
      Saves a file in the 'downloaded_files' directory.

      Args:
            fileData (bytes): The data to be saved in the file.
            fileName (str): The name with which the file will be saved.
      '''
      filePath = os.path.join('downloaded_files', fileName)
      with open(filePath, 'wb') as f:
            f.write(fileData)
      print(f"File saved at: {filePath}") 

def getComsType():
      '''
      Asks the user to specify the communication type to be used.
      '''
      while True:
            server_type = input('UDP or TCP?\n').strip().lower()
            if server_type in ['udp', 'tcp']:
                  return server_type
            else:
                  print('invalid input')

def initializeClient() :
      '''
      Gets the username to register and sends it to the server.
      '''
      global myName
      clearTerminal()
      myName = input('What is your name?\n').strip()
      client.sendMessage(message="['{}','server','register',['','']]<END>".format(myName).encode('utf-8'))
      serverMessage = receiveSingleMessage()
      manageResponse(serverMessage)

def decodeMessage(serverMessage):
      '''
      Decodes received messages.

      The client processes the message and the server address.

      The message protocol used by the server and clients is as follows:
      ['sender', 'receiver', 'operation', ['messageType', message (one or more fields)]]<END>

      Args:
            serverMessage (tuple): A tuple containing the encoded message (bytes) and the server address, which is also a tuple containing the IPv4 address (str) and the port (int) where the server socket is running.

      Returns:
            sender (str): The name of the sender.
            receiver (str): The name of the intended recipient (even though every message is managed by the server).
            operation (str): The type of operation being requested or performed.
            messageType (str): The type or content of the message.
            message (list): A list containing the message(s).
      '''
      try:
            sMessage = serverMessage[0]
            sMessage = sMessage.rstrip(b"<END>")
            messageReceived = ast.literal_eval(sMessage.decode('utf-8'))
            sender = messageReceived[0]
            receiver = messageReceived[1]
            operation = messageReceived[2]
            messageContent = messageReceived[3]
            messageType = messageContent[0]
            message = []
            for i in range(1,len(messageContent)):
                  message.append(messageContent[i])
            return sender, receiver, operation, messageType, message
      except SyntaxError as e:
            print(f"Syntax error: {e}")
      except ValueError as e:
            print(f"Value error: {e}")
      except Exception as e:
            print(f"Error: {e}")

def manageResponse(serverMessage):
      '''
      Manages the client's response to a received message.

      First, decodes the message and then checks the operation:
            - response: The server is responding to an operation made by the client.
            - new_convo: Another client wants to communicate with this client. This functionality is not implemented.
            - message: The connected client sent a message or file to this client.

      Args:
            serverMessage (tuple): A tuple containing the encoded message (bytes) and the server address, which is also a tuple containing the IPv4 address (str) and the port (int) where the server socket is running.
      '''
      global connected, messagesList, serverAddress, filesList
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
                  clientMessage = "['{}','{}','response',['new_convo','accepted']]<END>".format(myName, message[0]).encode('utf-8')
                  client.sendMessage(clientMessage)
            elif messageType == "new_convo":
                  if message[0] == "wait":
                        # print("There is no current contact with this name.\n")
                        # clientChoice = input("Do you wish to: wait(w), make new connection(c) or to quit(q)?")
                        # while clientChoice != "w" and clientChoice != "c" and clientChoice != "q":
                        #       print("Please, make a valid choice.")
                        #       clientChoice = input("Do you wish to: wait(w), make new connection(c) or to quit(q)?")
                        # if clientChoice == "w":
                        #       clientMessage = "['{}','server','response',['wait','ok']]<END>".format(myName).encode('utf-8')
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
            elif messageType == "file":
                  for msg in messagesList:
                        if str(msg[1]) == message[0] and msg[2] == "file":
                              msg[4] = message[1]
                              myScreen(True)
                              break
            elif messageType == "download-list":
                  print("Choose a file: (--cancel to abort the operation)")
                  for file in message:
                        print(f"- {file}")

                  fileName = input()

                  while not fileName in message or fileName == "--cancel":
                        if fileName == "--cancel":
                              return
                        fileName = input("please, choose a valid file\n")
                  
                  clientMessage = "['{}','server','download',['file','{}','{}']]<END>".format(myName, connectionName, fileName).encode('utf-8')
                  client.sendMessage(clientMessage)
            elif messageType == "download":
                  fileId = message[0]
                  fileName = message[1]
                  more_chunks = message[2]
                  offset = message[3]
                  chunk = message[4]
                  finished = False
                  if not more_chunks:
                        finished = True
                  
                  if int(offset) == 0:
                        newFile = [sender, receiver, messageId, fileName, finished, chunk, 0]
                        filesList.append(newFile)
                  else:
                        foundFile = next((file for file in filesList if file[2] == messageId), None)
                        if foundFile:
                              if int(offset) == len(foundFile[5]):
                                    foundFile[5] += chunk  # Concatenar o novo chunk ao arquivo
                                    foundFile[6] = int(offset) + len(chunk)  # Atualiza o offset
                                    if finished: # se nao houver mais chunks
                                          foundFile[4] = True
                                          saveFiles(fileData=foundFile[5], fileName=foundFile[3])
                                          matching_message = next((msg for msg in messagesList if msg[0] == connectionName and msg[1] == fileId and msg[2] == "file" and msg[3] == fileName), None)
                                          matching_message[4] = "downloaded"
                                          filesList.remove(foundFile)
                              else:
                                    matching_message = next((msg for msg in messagesList if msg[0] == connectionName and msg[1] == fileId and msg[2] == "file" and msg[3] == fileName), None)
                                    matching_message[4] = "error"
                                    filesList.remove(foundFile)
                        else:
                              matching_message = next((msg for msg in messagesList if msg[0] == connectionName and msg[1] == fileId and msg[2] == "file" and msg[3] == fileName), None)
                              matching_message[4] = "error"
      elif operation == "new_convo":
            if messageType == "contact":
                  clearTerminal()
                  print("{} wants to begin a new contact with you!".format(str(message[0]).capitalize()))
                  answer = ""
                  while answer.lower() != 'n' and answer.lower() != 'y':
                        answer = input("Do you want to connect? (y or n)\n")
                  if answer.lower() == 'n':
                        client.sendMessage("['{}','{}','response',['new_convo','denied']]<END>".format(myName, sender).encode('utf-8'), serverAddress)
                  else:
                        client.sendMessage("['{}','{}','response',['new_convo','accepted']]<END>".format(myName, sender).encode('utf-8'), serverAddress)
      elif operation == "message":
            if messageType == "message":
                  messagesList.append([connectionName, message[0], messageType, message[1]])
                  if message[0] == len(messagesList):
                        print("\033[91mWe probably lost some message(s) along the way\033[0m")
                  myScreen(True)
            elif messageType == "file":
                  state = "not-downloaded"
                  messagesList.append([connectionName, message[0], messageType, message[1], state])
                  myScreen(True)

def connect():
      '''
      Asks the client whom they wish to connect with and sends the name to the server.
      '''
      global connectionName
      friendName = input("Who do you wish to connect with? Write their name!\n")
      
      while friendName == "":
            myScreen(False)
            print ("The name can not be empty")
            friendName = input("Who do you wish to connect with? Write their name!\n")

      connectionName = friendName
      myScreen(False)
      print("Waiting connection with {}...".format(connectionName))

      clientMessage = "['{}','server','new_convo',['contact','{}']]<END>".format(myName, connectionName).encode('utf-8')
      client.sendMessage(clientMessage)
      serverMessage = receiveSingleMessage()
      manageResponse(serverMessage=serverMessage)

def receiveSingleMessage():
      '''
      Receives a single message and then stops listening.

      Returns:
            serverMessage (tuple): A tuple containing the encoded message (bytes) and the server address, which is also a tuple containing the IPv4 address (str) and the port (int) where the server socket is running.
      '''
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
      '''
      Keeps listening to the server and receiving messages. Ensures that only a single, complete message is passed along.
      '''
      buffer = b""
      running = True
      while running:
            try:
                  if stop_event.is_set():
                        running = False
                  else:
                        serverMessage, address = client.receiveMessage()
                        if serverMessage is not None:
                              buffer += serverMessage
                              while b"<END>" in buffer:
                                    message, buffer = buffer.split(b"<END>", 1)
                                    manageResponse(serverMessage=(message, address))
            except socket.timeout:
                  time.sleep(0.1)
            except Exception as e:
                  print(f"An error occurred: {e}")
                  running = False

def uploadFile():
      '''
      Client command to upload a file to the server. Chooses the file from the 'files_to_send' directory.

      If the selected file is larger than 1024 bytes, it is fragmented before being sent to the server.
      '''
      global messageId, messagesList
      directory = 'files_to_send'
      files = os.listdir(directory)
      
      if files:
            print("Choose a file: (--cancel to abort the operation)")
            for file in files:
                  print(f"- {file}")

            fileName = input()

            while not fileName in files or fileName == "--cancel":
                  if fileName == "--cancel":
                        myScreen(True)
                        return
                  fileName = input("please, choose a valid file\n")
            
            messageId += 1
            file_path = os.path.join(directory, fileName)
            # stores message of file sent. State gets updated as received or not by the server
            state = "sent"
            messagesList.append([myName, messageId,"file",fileName,state])
            myScreen(True)

            with open(file_path, 'rb') as file:
                  file.seek(0, os.SEEK_END)
                  file_size = file.tell()
                  file.seek(0)
                  total_readed = 0
                  more_chunks = 1
                  while chunk := file.read(1024):
                        offset = total_readed
                        total_readed += len(chunk)
                        if total_readed == file_size:
                              more_chunks = 0
                        # sends [sender, receiver, opetation(message), [messageType(file), messageId, more_chunks, offset, chunk]]
                        clientMessage = "['{}','{}','message',['file','{}','{}',{},'{}',{}]]<END>".format(myName,connectionName,messageId,fileName,more_chunks,offset,chunk).encode('utf-8')
                        client.sendMessage(clientMessage)
      else:
            print("There are no files in 'files_to_send'")
            time.sleep(3)

def downloadFile():
      '''
      Client command to download a file sent by their connection. The client requests the server to list the available files for download. The download sequence is handled in messageResponse.
      '''
      clientMessage = "['{}','server','download',['list','{}']]<END>".format(myName, connectionName, ).encode('utf-8')
      client.sendMessage(clientMessage)
      running = True
      while running:
            try:
                  serverMessage = client.receiveMessage()
                  running = False
                  manageResponse(serverMessage=serverMessage)
            except socket.timeout:
                  time.sleep(0.1)
      myScreen(True)

def waitEntry():
      '''
      Waits for user input. There are special commands. If the user sends something that is not a command and is not blank, the client sends it as a message.

      The commands are:
            - exit: Quits the application.
            - upload: Sends a file to the server.
            - download: Fetches a file from the server sent by the connection.
            - help: Displays the list of commands on the screen.
            - cancel: Aborts the current operation.
      '''
      global messagesList, messageId
      while True:
            entry = input()
            if entry == "":
                  myScreen(True)
            elif entry == "--exit":
                  print("finishing run\n")
                  stop_event.set()
                  break
            elif entry == "--upload":
                  uploadFile()
            elif entry == "--download":
                  downloadFile()
            elif entry == "--help":
                  myScreen(True)
                  print("App client commands:\n\t'--upload' to choose a file from the 'files_to_send' folder to send to your contact\n\t'--download' to choose a file that your contact has sent to you to download to 'downloaded_files'\n\t'--exit' to quit the application\n\t'--cancel' to close the help instructions")
            elif entry == "--cancel":
                  myScreen(True)
            else:
                  messageId += 1
                  clientMessage = "['{}','{}','message',['message','{}','{}']]<END>".format(myName, connectionName, messageId, entry).encode('utf-8')
                  client.sendMessage(clientMessage)
                  messagesList.append([myName, messageId,"message",entry])
                  myScreen(True)
      
def closeConnection():
      '''
      Sends a message to the server indicating that the connection will be closed, then closes the socket.
      '''
      clientMessage = "['{}','server','bye_bye',['','']]<END>".format(myName).encode('utf-8')
      client.sendMessage(clientMessage)
      client.closeConnection()

def start():
      '''
      Manages the app's runtime.

      Initializes global variables, including the socket.

      The socket runs in a separate thread.
      '''
      global client, stop_event, connected, messageId, filesList
      createDirectories()
      client = None
      connected = False
      messageId = 0
      filesList = []
      stop_event = threading.Event()
      clearTerminal()
      try:
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
      except Exception as e:
            print("Error: {}".format(e))

start()