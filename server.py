import socket
from time import sleep
from os import path
from sys import argv
from subprocess import Popen, PIPE

class Server:
	def __init__(self, sock, host, port, connections=1):
		self.sockServer = sock
		self.host = host
		self.port = port
		self.connections = connections
		self.banner = f"""
\033[1;34m{'=-'*10} Comandos disponíveis {'=-'*10}\033[m
\033[0;33m help\033[m-> Exibe esse menu
\033[0;33m ls\033[m-> Lista arquivos
\033[0;33m get\033[m-> Baixa arquivo: get <filename>
\033[0;33m exit\033[m-> Fecha conexão
"""

	def __send_file(self, filename, conn):
		if path.exists(path.abspath(filename)):

			with open(filename, 'rb') as file:
				msg_ok = 'ACK'.encode()
				filename = filename.encode()
				conn.send(msg_ok)
				sleep(1)
				conn.send(filename)
				sleep(1)

				for line in file.readlines():
					conn.send(line)
				else:
					print('\033[1;32m[+] Enviado com sucesso')
					msg_control = 'FIN'.encode()
					sleep(1)
					conn.send(msg_control)

		else:
			msg_not_exists = 'RST'.encode()
			conn.send(msg_not_exists)

	def __send_folder(self):
		...

	def __handler(self, conn, addr) -> None:
		while True:
			try:
				cmd = conn.recv(1024).decode().split(' ')
			except:
				pass

			match cmd[0]:
				case 'exit':
					conn.close()
					print('\033[1;32m[+] Conexão encerrada\033[m\n')
					break
				case 'help':
					conn.send(self.banner.encode())
				case 'ls':
					popen = Popen('ls', stdout=PIPE, stderr=PIPE)
					output, errors = popen.communicate(timeout=15)
					conn.send(output)
				case 'get':
					self.__send_file(cmd[1], conn)

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
