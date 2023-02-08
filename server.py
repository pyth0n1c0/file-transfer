import socket
from sys import argv
from subprocess import Popen, PIPE

class Server:
	def __init__(self, sock, host, port, connections=1):
		self.sockServer = sock
		self.host = host
		self.port = port
		self.connections = connections
		self.banner = f"""
[+] Connected\n
{'=-'*10} MENU {'=-'*10}
1) Listar arquivos
2) Sair
		"""
	
	def handler(self, conn, addr) -> None:
		option = 0

		if option != 2:
			option = int(conn.recv(1024).decode())
			print(f'{addr} -> {option}')
			#conn.send(b'[!] Invalid input!')
			
			proc = Popen('ls', stdout=PIPE, stderr=PIPE)
			output, errors = proc.communicate(timeout=15)
			str_output = output.decode()
			conn.send(output)

			print(str_output, errors)

	def run(self) -> None:
		print(type(self.host), type(self.port)) #-->
		
		self.sockServer.bind( (self.host, self.port) )
		self.sockServer.listen(self.connections)

		connection, addrClient = self.sockServer.accept()
		with connection as conn:

			print('[+] Connection:', addrClient[0], addrClient[1]) #-->

			conn.send(self.banner.encode())
			self.handler(conn, addrClient)

	def debbug(self) -> None:
		print(self.__dict__)


try:
	SERVER_IP = 'localhost'
	SERVER_PORT = int(argv[1])
except:
	print(f'Usage: python3 {argv[0]} <PORT>')
	exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server = Server(sock, SERVER_IP, SERVER_PORT)
server.debbug()
server.run()
