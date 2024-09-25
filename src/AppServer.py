import ast
import os
import socket
import threading
import time
from server.UDPserver import UDPserver
from server.TCPserver import TCPserver

serverPort = 12000

global masterServer, coms_type, clientsList, clientAddress, portCounter, serverThreads, filesList

def clearTerminal():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux or macOS
        os.system('clear')

def createDirectory():
      directory = "server_files"
      if not os.path.exists(directory):
            os.makedirs(directory)

def saveFiles(fileData, fileName):
      filePath = os.path.join('server_files', fileName)
      with open(filePath, 'wb') as f:
            f.write(fileData)
      print(f"File saved at: {filePath}") 

def waitEntry():
      while True:
            entry = input('Press \'q\' to stop \n\n')
            if entry == 'q':
                  print('finishing run \n')
                  # masterServer.closeSocket()
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
      buffer = b""
      running = True
      while running:
            try:
                  clientMessage, clientAddress = server.receiveMessage()
                  if clientMessage is not None:
                        buffer += clientMessage
                        while b"<END>" in buffer:  # Verifica se há uma mensagem completa (delimitada)
                              # Divide o buffer pela primeira ocorrência de <END>
                              message, buffer = buffer.split(b"<END>", 1)  
                              handleMessage(message) # Passa a mensagem completa para ser processada
            except socket.timeout:
                  time.sleep(0.1)
            except ConnectionResetError:
                  print(f"Connection reset by client: {clientAddress}\n")
            except Exception as e:
                  print(f"An error occurred: {e}")

def decodeMessage(clientMessage):
      try:
            clientMessage = clientMessage.rstrip(b"<END>")
            messageReceived = ast.literal_eval(clientMessage.decode('utf-8'))
            sender = messageReceived[0]
            receiver = messageReceived[1]
            operation = messageReceived[2]
            messageContent = messageReceived[3]
            messageType = messageContent[0]
            message = []
            for i in range(1,len(messageContent)):
                  message.append(messageContent[i])
            return sender, receiver, operation, messageType, message, clientAddress
      except SyntaxError as e:
            print(f"Syntax error: {e}")
      except ValueError as e:
            print(f"Value error: {e}")
      except Exception as e:
            print(f"Error: {e}")

def sendMessageToClient(client, clientMessage):
      for clnt in clientsList:
            if clnt[0] == client:
                  clnt[1].sendMessage(clientMessage, clnt[2])
                  break

def handleMessage(clientMessage):
      global portCounter, filesList
      sender, receiver, operation, messageType, message, clientAddress = decodeMessage(clientMessage)
      if operation == "register":
            for client in clientsList:
                  if client[0] == sender:
                        if client[2] != '':
                              response = "['server','{}','response',['register','already_registered']]<END>".format(sender).encode('utf-8')
                              masterServer.sendMessage(response, clientAddress)
                              return
                        else:
                              for connection in clientsList:
                                    if connection[3] == sender:
                                          newServerSocket = None
                                          portCounter = portCounter + 1
                                          port = serverPort + portCounter
                                          if coms_type == 'udp':
                                                newServerSocket = UDPserver(serverPort=port, client=sender)
                                          else:
                                                newServerSocket = TCPserver(serverPort=port, client=sender)
                                          newServerThread = threading.Thread(target=runServer, args=(newServerSocket,))
                                          newServerThread.daemon = True
                                          newServerThread.start()
                                          serverThreads.append(newServerThread)
                                          clientsList.append([sender, newServerSocket, clientAddress, ''])
                                          response = "['server','{}','response',['register-connection','{}', {}]]<END>".format(sender, connection[3], str(port)).encode('utf-8')
                                          masterServer.sendMessage(response, clientAddress)
                                          # sendMessageToClient(client=sender, clientMessage=response)
                                          print ("Registered: {}, {}\n".format(sender, str(clientAddress)))
                                          return

            newServerSocket = None
            portCounter = portCounter + 1
            port = serverPort + portCounter
            if coms_type == 'udp':
                  newServerSocket = UDPserver(serverPort=port, client=sender)
            else:
                  newServerSocket = TCPserver(serverPort=port, client=sender)
            newServerThread = threading.Thread(target=runServer, args=(newServerSocket,))
            newServerThread.daemon = True
            newServerThread.start()
            serverThreads.append(newServerThread)
            clientsList.append([sender, newServerSocket, clientAddress, ''])
            response = ("['server','{}','response',['register','registered', '{}']]<END>".format(sender, str(port))).encode('utf-8')
            masterServer.sendMessage(response, clientAddress)
            print ("Registered: {}, {}\n".format(sender, str(clientAddress)))
      elif operation == "new_convo":
            contact_exists = any(message[0] == client[0] for client in clientsList) #confere se contato requerido ja existe
            for c in clientsList:
                  if c[0] == sender:
                        c[3] = message[0] #nome do contato requerido
            if contact_exists:
                  contact = next((client for client in clientsList if client[0] == message[0]), None) #busca contato requerido, caso exista
                  if contact[3] == sender:
                        response = "['{}','{}','response',['new_convo','accepted']]<END>".format(sender, contact[0]).encode('utf-8')
                        sendMessageToClient(client=contact[0], clientMessage=response)
                        response = "['{}','{}','response',['new_convo','accepted']]<END>".format(contact[0], sender).encode('utf-8')
                        sendMessageToClient(client=sender, clientMessage=response)
                        print("New convo between {} and {}\n".format(contact[0], sender))
                  elif contact[3] != '':
                        response = "['server','{}','response',['new_convo','denied']]<END>".format(sender).encode('utf-8')
            else:
                  response = "['server','{}','response',['new_convo','wait']]<END>".format(sender).encode('utf-8')
                  sendMessageToClient(client=sender, clientMessage=response)
      elif operation == "message":
            contact = next((client for client in clientsList if client[0] == sender), None)
            connection = next(client for client in clientsList if client[0] == contact[3])
            if messageType == "message":
                  serverMessage = "['{}','{}','message',['message', '{}', '{}']]<END>".format(sender, contact[3], message[0], message[1]).encode('utf-8')
                  sendMessageToClient(client=contact[3], clientMessage=serverMessage)
            elif messageType == "file":
                  messageId = message[0]
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
                        print("new file being received from {}".format(sender))
                  else:
                        foundFile = None
                        for file in filesList:
                              if file[0] == sender and file[1] == receiver and file[2] == messageId:
                                    foundFile = file
                                    break
                        if foundFile:
                              if int(offset) == len(foundFile[5]):
                                    foundFile[5] += chunk  # Concatenar o novo chunk ao arquivo
                                    foundFile[6] = int(offset) + len(chunk)  # Atualiza o offset
                                    if finished: # se nao houver mais chunks
                                          foundFile[4] = True
                                          saveFiles(fileData=foundFile[5], fileName=foundFile[3])
                                          serverMessage = "['server','{}','response',['file', '{}', 'received']]<END>".format(sender, messageId).encode('utf-8')
                                          sendMessageToClient(client=sender, clientMessage=serverMessage)
                                          serverMessage = "['{}','{}','message',['file', '{}', '{}']]<END>".format(sender, receiver, messageId, foundFile[3]).encode('utf-8')
                                          sendMessageToClient(client=receiver, clientMessage=serverMessage)
                              else:
                                    # Trate o erro ou ignore se o offset não for igual ao tamanho do chunk atual
                                    print(f"Offset mismatch: expected {len(foundFile[5])}, but got {offset}")
                                    serverMessage = "['server','{}','response',['file', '{}', 'error']]<END>".format(sender, messageId).encode('utf-8')
                                    sendMessageToClient(client=sender, clientMessage=serverMessage)
                        else:
                              # Caso não encontre o arquivo correspondente, trate o erro ou crie um novo
                              print("Previous packages from {}'s file no found. Package loss!!".format(sender))
                              serverMessage = "['server','{}','response',['file', '{}', 'error']]<END>".format(sender, messageId).encode('utf-8')
                              sendMessageToClient(client=sender, clientMessage=serverMessage)
      elif operation == "bye_bye":
            contact = next((client for client in clientsList if client[0] == sender), None)
            if contact != None:
                  if contact[3] != "":
                        connection = next(client for client in clientsList if client[0] == contact[3])
                        if connection[3] == contact[0]:
                              connection[3] = ""
                              response = "['server','{}','disconnect',['disconnect','{}']]<END>".format(connection[0], sender).encode('utf-8')
                              sendMessageToClient(client=connection[0], clientMessage=response)
                  contact = None
                  print ("{} disconnected".format(sender))
      elif operation == "response":
            if messageType == "new_convo":
                  if message[0] == "accepted":
                        contact = next((client for client in clientsList if client[0] == message), None)
                        response = "['{}','{}','response',['new_convo','accepted']]<END>".format(sender, receiver).encode('utf-8')
                        sendMessageToClient(client=receiver, clientMessage=response)
      elif operation == "download":
            if messageType == "list":
                  titles = [f"'{file[2]}-{file[3]}'" for file in filesList if file[0] == message[0] and file[1] == sender]
                  # Junta os títulos em uma string separada por vírgulas
                  titles_str = ', '.join(titles)
                  # Formata a mensagem no formato desejado
                  serverMessage = "['server','{}','response',['download-list', {}]]<END>".format(sender, titles_str).encode('utf-8')
                  sendMessageToClient(client=sender, clientMessage=serverMessage)
def start():
      global masterServer, clientsList, coms_type, portCounter, serverThreads, filesList
      clientsList = []
      filesList = []
      serverThreads = []
      portCounter = 0
      createDirectory()
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
      masterServerThread = threading.Thread(target=runServer, args=(masterServer,))
      masterServerThread.daemon = True
      masterServerThread.start()
      waitEntry()

start()