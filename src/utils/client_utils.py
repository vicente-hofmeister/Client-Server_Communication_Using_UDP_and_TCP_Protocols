import ast

def initialize_client() :
      myName = input('What is your name?')

      return "['register',['name','{}']]".format(myName).encode()

def manageResponse(receivedMessage: bytes, serverAddress):
      message = ast.literal_eval(receivedMessage.decode())
      operation = message[0]
      messageContent = message[1]

      if operation == "reponse":
            if messageContent[0] == "registered":
                  return (choose_firend(), serverAddress)

def choose_firend():
      
      friendName = input("Wish to connect with someone? Write their name!")
      return "['new_convo',['contact','{}']]".format(friendName).encode()