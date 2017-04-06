#! /usr/bin/python

"""
A simple server that gets a message from its client and sends a message entered
by the user, repeating until the user exits with an interrupt or an EOF.
"""

import socket

host = "localhost"
port = 12345
running = True
server = socket.socket()

server.bind( (host, port) )
server.listen(5)

client, address = server.accept()
print "Incoming connection from", address

try:
	while running:
		received = client.recv(1024)

		if received:
			print "Client>", received
			user_input = raw_input("Server> ")
			client.send(user_input)

		else:
			running = False

except (EOFError, KeyboardInterrupt):
	print "Good bye!"

finally:
	client.close()
	server.close()
