import socket
from sys import argv

class Client:
	def __init__(self, sock, host, port):
		self.sockClient = sock
		self.host = host
		self.port = port

	def run(self) -> None:
		self.sockClient.connect( (self.host, self.port) )
		banner = self.sockClient.recv(1024).decode()
		print(banner)
		
		cmd = ''
		#while cmd != b'2':
		cmd = input('server>').encode()
		self.sockClient.send(cmd)
		response = self.sockClient.recv(1024).decode()
		print(response)
		#else:
		self.sockClient.close()

	def debbug(self) -> None:
		print(self.__dict__)


try:
	SERVER_IP = argv[1]
	SERVER_PORT = int(argv[2])
except:
	print(f'Usage: python3 {argv[0]} <SERVER_IP> <SERVER_PORT>')
	exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client = Client(sock, SERVER_IP, SERVER_PORT)
client.run()
