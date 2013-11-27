#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Fellipe Silveira
# Rodrigo Dumont

import socket
import os
import sys
import random

SERVER_PORT = 4200 # ALL THE SERVERS RUN ON THE SAME PORT
SERVER_1 = 'macalan.c3sl.ufpr.br'
SERVER_2 = 'priorat.c3sl.ufpr.br'
SERVER_3 = 'bowmore.c3sl.ufpr.br'

def connectToServer(count):
	if sys.argv[1] == 1:
		count = ramdom.randint(1,3)

	if count == 1:
		serverName = 'macalan.c3sl.ufpr.br'
	elif count == 2:
		serverName = 'priorat.c3sl.ufpr.br'
	elif count == 3:
		serverName = 'bowmore.c3sl.ufpr.br'

	# CONNECTING TO SERVER
	aServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	aServer.connect((serverName, SERVER_PORT))
	print 'Conectado com o Servidor X'
	# CONNECTED TO SERVER

	return aServer

if len(sys.argv) != 2:
	print 'Modo correto de execução: ./portal X\nonde X: 1=Aleatorio e 2=RoundRobin'
	sys.exit()

rr_count = 1

HOST = ''				# Portal IP
PORT = 5001				# Portal Port
portal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
portal.bind((HOST, PORT))
portal.listen(5)
while True:
	con, client = portal.accept()
	
	# INCREASE ROUND ROBIN VARIABLE 
	if sys.argv[1] == 2:
		rr_count += 1%3

	pid = os.fork()
	if pid == 0:
		portal.close()
		print 'Conectado com o Cliente:', client

		# RECEIVING FILE FROM CLIENT
		print 'Recebendo arquivo fonte do Cliente: {}'.format(client)
		aFile = open('./portal_in.txt', 'wb')
		msg = con.recv(1024)
		while msg:
			aFile.write(msg)
			#print client, msg
			if msg[-3:] == 'FIM': break
			msg = con.recv(1024)
		aFile.close()
		print 'Arquivo fonte recebido com sucesso do Cliente: {}'.format(client)
		# FILE RECEIVED FROM CLIENT

		# CONNECTING TO SERVER
		# HOST = ''		# Server IP
		# PORT = 5003		# Server Port
		# aServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# aServer.connect((HOST, PORT))
		# print 'Conectado com o Servidor X'

		aServer = connectToServer(rr_count)

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
			if msg[-3:] == 'FIM': break
			msg = aServer.recv(1024)
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