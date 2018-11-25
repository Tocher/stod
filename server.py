import json, socket, select

def send_to_all (sock, message):
	for socket in connected_list:
		if socket != server_socket and socket != sock :
			try :
			    to_json(socket, message)
			except :
				# if connection not available
				socket.close()
				connected_list.remove(socket)

def to_json (sock, message):
	sock.send(bytes(json.dumps(message)))

if __name__ == "__main__":
	name=""
	record={}
	connected_list = []
	buffer = 4096
	port = 5001

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server_socket.bind(("localhost", port))
	server_socket.listen(10)

	connected_list.append(server_socket)

	print "\33[32m \t\t\t\tSERVER WORKING \33[0m"

	while 1:
		rList,wList,error_sockets = select.select(connected_list,[],[])

		for sock in rList:
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				jsonData = sockfd.recv(buffer)
				name = json.loads(jsonData)
				connected_list.append(sockfd)
				record[addr]=""

				if name in record.values():
					to_json(sockfd, "\r\33[31m\33[1m Username already taken!\n\33[0m")
					del record[addr]
					connected_list.remove(sockfd)
					sockfd.close()
					continue
				else:
					record[addr]=name
					print "Client (%s, %s) connected" % addr," [",record[addr],"]"
					to_json(sockfd, "\33[32m\r\33[1m Welcome to chat room. Enter 'exit' anytime to exit\n\33[0m")

					send_to_all(sockfd, "\33[32m\33[1m\r "+name+" joined the conversation \n\33[0m")

			else:
				# Data from client
				try:
					jsonData = sock.recv(buffer)
					data1 = json.loads(jsonData)

					#print "sock is: ",sock
					data=data1[:data1.index("\n")]
					#print "\ndata received: ",data

					i,p=sock.getpeername()
					if data == "exit":
						msg="\r\33[1m"+"\33[31m "+record[(i,p)]+" left the conversation \33[0m\n"
						send_to_all(sock,msg)
						print "Client (%s, %s) is offline" % (i,p)," [",record[(i,p)],"]"
						del record[(i,p)]
						connected_list.remove(sock)
						sock.close()
						continue
					elif data == "list":
						msg="\r\33[1m"+"\33[35m Connected users:\33[0m\n"
						for rec in record:
						    msg=msg + "\r" + record[(rec[0], rec[1])] + "\n"
						to_json(sockfd, msg)
					else:
						msg="\r\33[1m"+"\33[35m "+record[(i,p)]+": "+"\33[0m"+data+"\n"
						send_to_all(sock,msg)

                #abrupt user exit
				except:
					(i,p)=sock.getpeername()
					send_to_all(sock, "\r\33[31m \33[1m"+record[(i,p)]+" left the conversation unexpectedly\33[0m\n")
					print "Client (%s, %s) is offline (error)" % (i,p)," [",record[(i,p)],"]\n"
					del record[(i,p)]
					connected_list.remove(sock)
					sock.close()
					continue

	server_socket.close()
