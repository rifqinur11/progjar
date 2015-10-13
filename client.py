import sys
import socket
import select
import time
import string

def chat_client():
	host = 'localhost'

	sys.stdout.write('Port : ')
	port = int(sys.stdin.readline())

	# create TCP/IP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# connect to remote host
	try :
		s.connect((host, port))
	except :
		print 'Gagal'
		sys.exit()
	
	print 'Client sudah terhubung'
	sys.stdout.write('Pesan: '); sys.stdout.flush()
	
	while 1:
		socket_list = [sys.stdin, s]
		# Get the list sockets which are readable
		ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
		for sock in ready_to_read:
			if sock == s:
				# incoming message from remote server, s
				data = sock.recv(4096)
				if not data :
					print '\nAnda tidak terhubung'
					sys.exit()
				else :
					#print data
					sys.stdout.write(data)
					sys.stdout.write('Pesan: '); sys.stdout.flush()
			else :
				# user entered a message
				msg = []
				temp = sys.stdin.readline()
				temp1 = string.split(temp[:-1])
				#menghitung jumlah input
				kata=len(temp1)

				if temp1[0]=="login" :
					if kata>2:
						print('Username hanya satu kata saja')
					elif kata<2:
						print('Masukkan username untuk login')
					else:
						s.send(temp)
			
				elif temp1[0]=="send" :
					if kata<3:
						print('Perintah salah')
					else:
						s.send(temp)

				elif temp1[0]=="sendall" :
					if kata<2:
						print("Perintah salah")
					else:
						s.send(temp)

				elif temp1[0]=="list" :
					if kata>1:
						print('Perintah salah')
					else:
						s.send(temp)

				else:
					print ('Perintah salah')

				sys.stdout.write('Pesan: '); sys.stdout.flush()
chat_client()
