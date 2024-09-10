import ast

clientsList = []

def handleMessage(messageFromClient: bytes, clientAddress):
      message = ast.literal_eval(messageFromClient.decode())
      operation = message[0]
      messageContent = message[1]

      if operation == "register":
            clientName = messageContent[1]
            clientsList.append([clientName,clientAddress])
            response = "['response',['registered','{}']]".format(str(clientAddress))
            print ("Registered: {}, {}".format(clientName, str(clientAddress)))

            return (response.encode(), clientAddress)
      elif operation == "new_convo":
            contactName = messageContent[1]

            contact_exists = any(contactName == client[0] for client in clientsList)
            
            if contact_exists:
                  response = "['response',['contact','allowed']]"
