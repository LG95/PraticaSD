#! /usr/bin/python

import socket

server = socket.socket()
host = "localhost"
port = 12345

server.bind( (host, port) )
server.listen(5)

try:
	while True:
		client, address = server.accept()
		print 'Incoming connection from', address
		client.send('Hello World!\n')
		client.close()

except KeyboardInterrupt:
	pass

finally:
	server.close()
