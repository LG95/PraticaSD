#! /usr/bin/python

""" A simple server that sends Hello World! to its clients. """

import socket

server = socket.socket()
host = "localhost"
port = 12345

server.bind( (host, port) )
server.listen(5)

try:
	while True:
		client, address = server.accept()
		print "Incoming connection from", address
		client.send("Hello World!")
		client.close()

except KeyboardInterrupt:
	print "Good bye!"

finally:
	server.close()
