import ast

clientsList = []

def handleMessage(messageFromClient: bytes, clientAddress):
      message = ast.literal_eval(messageFromClient.decode())
      sender = message[0]
      reciever = message[1]
      operation = message[2]
      messageContent = message[3]

      if operation == "register":
            clientsList.append([sender,clientAddress])
            response = "['server','{}','response',['register','registered']]".format(sender)
            print ("Registered: {}, {}".format(sender, str(clientAddress)))
            return (response.encode(), clientAddress)
      
      elif operation == "new_convo":
            contactName = messageContent[1]

            contact_exists = any(contactName == client[0] for client in clientsList)
            
            if contact_exists:

                  response = "['new_convo',['contact','{}']]".format()
            else:
                  response = "['response',['new_convo','not_allowed']]"