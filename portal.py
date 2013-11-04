#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Fellipe Silveira
# Rodrigo Dumont

import socket
import os
import sys

HOST = ''				# Server IP
PORT = 5001				# Server Port
portal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
portal.bind((HOST, PORT))
portal.listen(5)
while True:
	con, client = portal.accept()
	pid = os.fork()
	if pid == 0:
		portal.close()
		print 'Conectado por', client
		aFile = open('portal_in.txt', 'wb')
		msg = con.recv(1024)
		while msg:
			aFile.write(msg)
			print client, msg
			msg = con.recv(1024)
			#if not msg: break
		print 'Finalizando conexao do cliente', client
		con.close()
		sys.exit(0)
	else:
		con.close()