#! /usr/bin/python

""" A simple client that prints a single message from the server. """

import socket

server = socket.socket()
host = "localhost"
port = 12345

server.connect( (host, port) )

try:
	print server.recv(1024)

except KeyboardInterrupt:
	print "Good bye!"

finally:
	server.close()
