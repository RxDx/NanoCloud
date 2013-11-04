#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import socket
import os
import sys

HOST = ''				# Endereco IP do Servidor
PORT = 5000				# Porta que o Servidor esta
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
while True:
	con, portal = server.accept()
	pid = os.fork()
	if pid == 0:
		server.close()
		print 'Conectado por', portal
		aFile = open('./server_in.txt', 'wb')
		msg = con.recv(1024)
		while msg:
			aFile.write(msg)
			print portal, msg
			msg = con.recv(1024)
			#if not msg: break
		print 'Finalizando conexao do cliente', portal
		con.close()
		sys.exit(0)
	else:
		con.close()