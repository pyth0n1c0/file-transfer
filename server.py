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
\033[1;32m{'=-'*10} Comandos disponíveis {'=-'*10}\033[m
\033[0;33m help\033[m-> Exibe esse menu 
\033[0;33m ls\033[m-> Lista arquivos
\033[0;33m get\033[m-> Baixa arquivo: get <filename>
\033[0;33m exit\033[m-> Fecha conexão
"""

	def __send_file(self):
		...

	def __send_folder(self):
		...
	
	def __handler(self, conn, addr) -> None:
		while True:
			try:
				cmd = conn.recv(1024).decode()
			except:
				pass
					
			match cmd:
				case 'exit':
					conn.close()
					print('\033[1;32m[+] Conexão finalizada\033[m\n')
					break
				case 'help':
					conn.send(self.banner.encode()) 

		"""cmd = ''
		while cmd != 'exit': # REFATORAR
			try:
				cmd = int(conn.recv(1024).decode())
				print(addr[0] + '->', cmd)
			except:
				pass

			print('CMD:', cmd)

			match cmd:
				case 'ls':	
					proc = Popen('ls', stdout=PIPE, stderr=PIPE)
					output, errors = proc.communicate(timeout=15)
					formated_output = f"{'-='*10} FILES {'=-'*10}\n".encode() + output
					conn.send(formated_output)
					print(output, errors)
		
		else:
			conn.close()
			print('[+] Conexão encerrada!')
		"""

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
server.run()
