#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Fellipe Silveira
# Rodrigo Dumont

import socket
HOST = '127.0.0.1'		# Portal IP
PORT = 5001				# Portal Port

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print 'Para sair use CTRL+X\n'

#msg = raw_input()
aFile = open('./client_out.txt', 'rb')
msg = aFile.read(1024)
#while msg != '\x18':
while msg:
	client.send(msg)
	msg = aFile.read()
	#msg = raw_input()

client.close()