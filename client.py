import socket
from time import sleep
from sys import argv

class Client:
	def __init__(self, sock, host, port):
		self.sock = sock
		self.host = host
		self.port = port

	def __recv_file(self):
		msg_response = self.sock.recv(1024).decode()
		if msg_response == 'ACK':
			sleep(1)
			filename = self.sock.recv(1024).decode()
			sleep(1)
			print(f'\033[1;32m[+] Enviando arquivo:\033[m \033[35m{filename}\033[m')

			with open(filename, 'wb') as file:
				while True:
					data = self.sock.recv(1024)
					if data == b'FIN':
						break
					else:
						file.write(data)

					# Mostra cada recv(1024) do arquivo enviado
					#print('BEGIN') #!
					#print(data)
					#print('END')
				else:
					print('\033[1;32m[+]\033[m Arquivo enviado com sucesso!')


		elif msg_response == 'RST':
			print('\033[1;31m[-]\033[m Arquivo inexistente')

	def __handler(self):
		cmd = ''
		while cmd != 'exit':
			cmd = input('server>').lower()
			self.sock.send(cmd.encode())

			if cmd[:3] == 'get':
				self.__recv_file()

			elif cmd == 'ls':
				print(f"\033[1;34m{'-='*10} FILES {'=-'*10}\033[m")
				files = self.sock.recv(1024).decode()
				print(files)
			else:
				try:
					#! Fazer esperar só por alguns segundos
					response = self.sock.recv(1024).decode()
					print(response)
				except:
					pass
		else:
			self.sock.close()
		print('\033[1;32m[+] Conexão encerrada\033[m\n')

	def run(self) -> None:
		self.sock.connect( (self.host, self.port) )
		banner = self.sock.recv(1024).decode()
		print('\033[1;32m[+] Connected\033[m')

		print(banner)
		self.__handler()

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
