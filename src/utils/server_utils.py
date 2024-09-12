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
                  contact = next(client for client in clientsList if client[0] == contactName)
                  response = "['{}','{}','new_convo',['contact','{}']]".format(sender, contact[0], sender)
                  return (response.encode(), contact[1])
            else:
                  response = "['server','{}','response',['new_convo','not_allowed']]".format(sender)
                  return (response.encode(), clientAddress)
      elif operation == "response":
            if messageType == "new_convo":
                  if message == "accepted":
                        contact = next(client for client in clientsList if client[0] == receiver)
                        response = "['{}','{}','response',['new_convo','accepted']]".format(sender, receiver)
                        print("New convo between {} and {}".format(receiver, sender))
                        return (response.encode(), contact[1])