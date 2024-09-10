import os
import threading
from server.UDPserver import UDPserver
from server.TCPserver import TCPserver

serverPort = 12000

def clear_terminal():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux or macOS
        os.system('clear')

def wait_entry():
      while True:
            entry = input('Press \'q\' to stop \n')
            if entry == 'q':
                  print('finishing run \n')
                  break

def get_coms_type():
      while True:
            server_type = input('UDP or TCP?\n').strip().lower()
            if server_type in ['udp', 'tcp']:
                  return server_type
            else:
                  print('invalid input\n')

clear_terminal()
coms_type = get_coms_type()
server = None
clear_terminal()
if coms_type == 'udp':
      server = UDPserver(serverPort=serverPort)
else:
      server = TCPserver(serverPort=serverPort)
serverThread = threading.Thread(target=server.start)
serverThread.daemon = True
serverThread.start()

wait_entry()