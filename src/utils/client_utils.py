import ast

global serverAddress

def initialize_client() :
      myName = input('What is your name?\n')

      return "['{}','server','register',[]]".format(myName).encode()

def check_register(receivedMessage):
      message = ast.literal_eval(receivedMessage[0].decode())
      sender = message[0]
      reciever = message[1]
      operation = message[2]
      messageContent = message[3]

      if messageContent[1] == 'registered':
            print("Registered!")
            return True
      
      return False

def manageResponse(receivedMessage: bytes, serverAddress):
      message = ast.literal_eval(receivedMessage.decode())
      # operation = message[0]
      # messageContent = message[1]

      # if operation == "reponse":
      #       if messageContent[0] == "new_convo" and messageContent[1] == "allowed":
      #             print("Connected!")

def choose_friend(serverAddress):
      friendName = input("Wish to connect with someone? Write their name!\n")
      return ("['new_convo',['contact','{}']]".format(friendName).encode(), serverAddress)