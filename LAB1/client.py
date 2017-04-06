#! /usr/bin/python

"""
A simple client that gets input from the user to send to a server and shows the
server's message, repeating until the user exits with an interrupt or an EOF.
"""

import socket

host = "localhost"
port = 12345
running = True
server = socket.socket()

server.connect( (host, port) )

try:
	while running:
		user_input = raw_input("Client> ")
		server.send(user_input)
		received = server.recv(1024)

		if received:
			print "Server>", received

		else:
			running = False

except (EOFError, KeyboardInterrupt):
	print "Good bye!"

finally:
	server.close()
