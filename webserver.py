import threading
import socket
import time
import sys

def get_file(nama):
	myfile = open(nama)
	return myfile.read()

class MemprosesClient(threading.Thread):
	def __init__(self,client_socket,client_address,nama):
		self.client_socket = client_socket
		self.client_address = client_address
		self.nama = nama
		threading.Thread.__init__(self)

	def run(self):
		message = ''
		while True:
			data = self.client_socket.recv(32)
			if data:
				message = message + data #collect seluruh data yang diterima
				print data
				if(data[0: -13] == 'GET /foto1 HTTP/1.1'):
					self.client_socket.send(get_file('mobil.jpg'))
					break
				if(data[0: -13] == 'GET /foto2 HTTP/1.1'):
					self.client_socket.send(get_file('mobil2.jpg'))
					break
				else:
					print "data gambar tidak ditemukan!"
					break
			else:
				break
		self.client_socket.close()

class Server(threading.Thread):
	def __init__(self):
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = ('localhost',1111)
		self.my_socket.bind(self.server_address)
		threading.Thread.__init__(self)
	
	def run(self):
		self.my_socket.listen(1)
		nomor=0
		while (True):
			self.client_socket, self.client_address = self.my_socket.accept()
			nomor=nomor+1
			#---- menghandle message cari client (Memproses client)
			my_client = MemprosesClient(self.client_socket, self.client_address, 'PROSES NOMOR '+str(nomor))
			my_client.start()
			#----
serverku = Server()
serverku.start()
