import sys
import socket
import select
import string

HOST = 'localhost'
SOCKET_LIST = []
NAME_LIST = []
RECV_BUFFER = 4096
PORT = 1111

def chat_server():
	sys.stdout.write('Port : ')
	PORT = int(sys.stdin.readline())
	#creating TCP/IP socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
	# binding the socket
	server_socket.bind((HOST, PORT))
	server_socket.listen(10)

	# add server socket object to the list of readable connections
	SOCKET_LIST.append(server_socket)
	
	print "Chat server dimulai dengan port " + str(PORT)
	while True:
		# get the list sockets which are ready to be read through select
		# 4th arg, time_out = 0 : poll and never block
		ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
		for sock in ready_to_read:
			# when new connection request received
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				SOCKET_LIST.append(sockfd)
				print "Client (%s, %s) tersambung" % addr
		
			# a message from a client, not a new connection
			else:
				# process data received from client,
				try:
					# receiving data from the socket.
					data = sock.recv(RECV_BUFFER)
					if data:
						#pemisah command dan message
						temp1 = string.split(data[:-1])
						d=len(temp1) #panjangnya temp1
						#pengecekan command
						if temp1[0]=="login" :
							log_in(sock, str(temp1[1]))

						elif temp1[0]=="send" :
							logged = 0 #cek sudah login/belum
							user = ""
							#x merupakan iterator sebanyak banyaknya isi array name_list
							for x in range (len(NAME_LIST)):
								#kalau alamat kita sudah ada di name_list jadi kamu sudah login
								if NAME_LIST[x]==sock:
									logged=1
									user=NAME_LIST[x+1]
							if logged==0:
								send_msg(sock, "Login diperlukan\n")
							else:
								temp2=""
								for x in range (len(temp1)):
									if x>1:
										if not temp2:
											temp2+=str(temp1[x])
										#jika pesannya panjang
										else:
											temp2+=" "
											temp2+=str(temp1[x])
								#mengirim ke target
								for x in range (len(NAME_LIST)):
									#temp1[1] nama target yang mau dikirim message
									if NAME_LIST[x]==temp1[1]:
										send_msg(NAME_LIST[x-1], "["+user+"] : "+temp2+"\n")
						
						elif temp1[0]=="sendall" :
							logged = 0
							user = ""
							for x in range (len(NAME_LIST)):
								if NAME_LIST[x]==sock:
									logged=1
									user=NAME_LIST[x+1]
							if logged==0:
								send_msg(sock, "Login diperlukan\n")
							else:
								temp2=""
								for x in range(len(temp1)):
									if x!=0:
										if not temp2:
											temp2=str(temp1[x])
										else:		
											temp2+=" "
											temp2+=temp1[x]
											broadcast(server_socket, sock, "["+user+"] : "+temp2+"\n")
						
						#lihat user yang terconnect
						elif temp1[0]=="list" :
							logged = 0
							for x in range (len(NAME_LIST)):
								if NAME_LIST[x]==sock:
									logged=1
							if logged==0:
								send_msg(sock, "Login diperlukan\n")
							else:
								temp2=""
								for x in range (len(NAME_LIST)):
									#nyari nama dari array name_list yang berada di index ganjil
									if x%2==1:
										temp2+=" "
										temp2+=str(NAME_LIST[x])
								send_msg(sock, "[List_User] : "+temp2+"\n")

						else:
							print ('Perintah salah')

					else:
						# remove the socket that's broken
						if sock in SOCKET_LIST:
							SOCKET_LIST.remove(sock)
							# at this stage, no data means probably the connection has been broken
							broadcast(server_socket, sock, "Client (%s, %s) terputus\n" % addr)

				# exception
				except:
					broadcast(server_socket, sock, "Client (%s, %s) terputus\n" % addr)
					continue
			
	server_socket.close()

# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
		for x in range (len(NAME_LIST)):
			# send the message only to peer
			if NAME_LIST[x] != server_socket and NAME_LIST[x] != sock and x%2==0 :
				try :
					NAME_LIST[x].send(message)
				except :
					# broken socket connection
					NAME_LIST[x].close()
					# broken socket, remove it
					if NAME_LIST[x] in SOCKET_LIST:
						SOCKET_LIST.remove(NAME_LIST[x])

def send_msg (sock, message):
	try:
		sock.send(message)
	except:
		sock.close()
		if sock in SOCKET_LIST:
			SOCKET_LIST.remove(sock)

def log_in (sock, user):
	a = 0
	b = 0
	for name in NAME_LIST:
		if name == user:
			a = 1
		if name == sock:
			b = 1
		if a==1:
			send_msg(sock, "Anda Sudah login\n")
		elif b==1:
			send_msg(sock, "Username sudah dipakai\n")
		else:
			#masukkan data user ke array
			NAME_LIST.append(sock)
			NAME_LIST.append(user)
			send_msg(sock, "Login berhasil\n")

chat_server()			


