#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Fellipe Silveira
# Rodrigo Dumont

import socket
HOST = '127.0.0.1'		# Server IP
PORT = 5001				# Server Port

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect((HOST, PORT))

print 'Para sair use CTRL+X\n'

#msg = raw_input()
aFile = open('./client_out.txt', 'rb')
if (not aFile):
	print 'Arquivo '+aFile
msg = aFile.read(1024)
#while msg != '\x18':
while msg:
	tcp.send (msg)
	msg = aFile.read()
	#msg = raw_input()

tcp.close()