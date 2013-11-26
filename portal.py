#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Fellipe Silveira
# Rodrigo Dumont

import socket
import os
import sys

HOST = ''				# Portal IP
PORT = 5001				# Portal Port
portal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
portal.bind((HOST, PORT))
portal.listen(5)
while True:
	con, client = portal.accept()
	pid = os.fork()
	if pid == 0:
		portal.close()
		print 'Conectado com o Cliente:', client

		# RECEIVING FILE FROM CLIENT
		print 'Recebendo arquivo fonte do Cliente: {} \n'.format(client)
		aFile = open('./portal_in.txt', 'wb')
		msg = con.recv(1024)
		while msg:
			aFile.write(msg)
			print client, msg
			msg = con.recv(1024)
			if msg[-3:] == 'FIM': break
		aFile.close()
		print 'Arquivo fonte recebido com sucesso do Cliente: {} \n'.format(client)
		# FILE RECEIVED FROM CLIENT

		# CONNECTING TO SERVER
		HOST = ''		# Server IP
		PORT = 5004		# Server Port
		aServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		aServer.connect((HOST, PORT))
		print 'Conectado com o Servidor X'
		# CONNECTED TO SERVER

		# SENDING FILE TO SERVER
		print 'Enviando arquivo fonte para o Servidor X.'
		aFile = open('./portal_in.txt', 'rb')
		msg = aFile.read(1024)
		while msg:
			aServer.sendall(msg)
			msg = aFile.read(1024)
		aFile.close()
		aServer.sendall('FIM')
		print 'Arquivo fonte enviado com sucesso para o Servidor X.'
		# FILE SENT TO SERVER

		# RECEIVING OUTPUT FROM SERVER
		print 'Recebendo saída do Servidor X'
		aFile = open('program_output2.txt', 'wb')
		msg = aServer.recv(1024)
		while msg:
			print 'Saída do Servidor X para o Cliente {} é {}'.format(client, msg)
			aFile.write(msg)
			msg = aServer.recv(1024)
			if msg[-3:] == 'FIM': break
		aFile.close()
		print 'Saída do Servidor X recebida com sucesso'
		# RECEIVED REPLY FROM SERVER

		# SENDING OUTPUT TO CLIENT
		print 'Enviando saída para o Cliente: {}'.format(client)
		aFile = open('program_output2.txt', 'rb')
		msg = aFile.read(1024)
		while msg:
			con.sendall(msg)
			msg = aFile.read(1024)
		aFile.close()
		con.sendall('FIM')
		print 'Saída enviada com sucesso para o Cliente: {}'.format(client)
		# OUTPUT SENT TO CLIENT

		print 'Finalizando conexao do Cleinte: {}'.format(client)
		con.close()
		sys.exit(0)
	else:
		con.close()
