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

	def __send_file(self):
		...

	def __send_folder(self):
		...
	
	def __handler(self, conn, addr) -> None:
		#try:
		option = 0
		while option != 2: # REFATORAR
			try:
				option = int(conn.recv(1024).decode())
				print(addr[0] + '->', option)
			except:
				pass

			proc = Popen('ls', stdout=PIPE, stderr=PIPE)
			match option:
				case 1:		
					output, errors = proc.communicate(timeout=15)
					formated_output = f"{'-='*10} FILES {'=-'*10}\n".encode() + output
					conn.send(formated_output)

			print(output, errors)
		else:
			conn.close()
			print('[+] Conexão encerrada!')
			#except:	
			...
#			conn.close()
#			print('[-] Conexão encerrada!')

	def run(self) -> None:
		self.sockServer.bind( (self.host, self.port) )
		self.sockServer.listen(self.connections)
		print(f'[+] Listening on {self.host} {self.port}')

		connection, addrClient = self.sockServer.accept()
		with connection as conn:
			print('[+] Connection:', addrClient[0], addrClient[1])
			conn.send(self.banner.encode())
			self.__handler(conn, addrClient)

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
