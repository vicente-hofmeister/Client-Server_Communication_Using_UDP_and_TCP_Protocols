from client.UDPclient import UDPclient
from client.TCPclient import TCPclient

serverName = '127.0.0.1'
serverPort = 12000

def get_coms_type():
      while True:
            server_type = input('UDP ou TCP?').strip().lower()
            if server_type in ['udp', 'tcp']:
                  return server_type
            else:
                  print('invalid input')

client = None

if get_coms_type() == 'udp':
      client = UDPclient(serverName=serverName, serverPort=serverPort)
else:
      client = TCPclient(serverName=serverName, serverPort=serverPort)

client.start()