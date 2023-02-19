import socket
from sys import argv

class Client:
	def __init__(self, sock, host, port):
		self.sock = sock
		self.host = host
		self.port = port

	def __handler(self):
		cmd = ''
		while cmd != 'exit':
			cmd = input('server>')
			self.sock.send(cmd.encode())
			try:
				response = self.sock.recv(1024).decode()
				print(response)
			except:
				pass
		else:
			self.sock.close()
		print('\033[1;32m[+] Conexão finalizada\033[m\n')
	
	def run(self) -> None:
		self.sock.connect( (self.host, self.port) )
		banner = self.sock.recv(1024).decode()
		print('\033[1;32m[+] Connected\033[m')

		print(banner)
		self.__handler()

		"""
		cmd = b''
		while cmd != b'exit\n':
			cmd = input('server>').encode()

			self.sock.send(cmd)
			print(cmd)
			response = self.sock.recv(1024).decode()
			print(response)

		else:
			self.sock.send(cmd)
			self.sock.close()
			print('[+] Conexão encerrada!')
		"""

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
