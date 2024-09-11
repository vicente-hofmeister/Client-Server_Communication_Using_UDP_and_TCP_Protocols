import ast

global clientsList, sender, receiver, operation, messageType, message, clientAddress
clientsList = []

def decodeMessage(clientMessage):
      global sender, receiver, operation, messageType, message, clientAddress
      messageReceived = ast.literal_eval(clientMessage[0].decode())
      sender = messageReceived[0]
      receiver = messageReceived[1]
      operation = messageReceived[2]
      messageContent = messageReceived[3]
      messageType = messageContent[0]
      message = messageContent[1]
      clientAddress = clientMessage[1]

def handleMessage(clientMessage):
      decodeMessage(clientMessage)
      if operation == "register":
            clientsList.append([sender,clientAddress])
            response = "['server','{}','response',['register','registered']]".format(sender)
            print ("Registered: {}, {}".format(sender, str(clientAddress)))
            return (response.encode(), clientAddress)
      elif operation == "new_convo":
            contactName = message
            contact_exists = any(contactName == client[0] for client in clientsList)
            
            if contact_exists:
                  return "['{}','{}','new_convo',['contact','{}']]".format(sender, contactName, sender)
            else:
                  return "['server','{}','response',['new_convo','not_allowed']]".format(sender)
      elif operation == "response":
            if messageType == "new_convo":
                  if message == "accepted":
                        return asdadsada