#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Fellipe Silveira
# Rodrigo Dumont

import socket
import os
import sys
import random
import subprocess

SERVER_PORT = 4224 # ALL THE SERVERS RUN ON THE SAME PORT
SERVER_1 = 'macalan.c3sl.ufpr.br'
SERVER_2 = 'priorat.c3sl.ufpr.br'
SERVER_3 = 'bowmore.c3sl.ufpr.br'

def connectToServer():
	rr_file = open('rr_count', 'rb')
	rr_count = rr_file.read(1)
	rr_file.close()

	print rr_count

	rr_count_int = int(rr_count)

	if sys.argv[1] == '1':
		random.seed(256)
		p = subprocess.Popen(["echo", "$[ 0 + $[ RANDOM % 3]]"], stdout=subprocess.PIPE)
		cmdOutput, err = p.communicate()
		print "aqui ta a saida: ", cmdOutput
		print '1', rr_count_int
		rr_count_int = str(cmdOutput)
		print '2',rr_count_int
		rr_count_int %= 3
		print 'random fucking moda fucker: ', rr_count_int

	if rr_count_int == 0:
		serverName = 'macalan.c3sl.ufpr.br'
	elif rr_count_int == 1:
		serverName = 'priorat.c3sl.ufpr.br'
	elif rr_count_int == 2:
		serverName = 'bowmore.c3sl.ufpr.br'

	# CONNECTING TO SERVER
	aServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	aServer.connect((serverName, SERVER_PORT))
	print 'Conectado com o Servidor', serverName
	# CONNECTED TO SERVER

	# INCREASE ROUND ROBIN VARIABLE
	rr_count_int += 1
	rr_count_int %= 3

	rr_count = str(rr_count_int)

	print 'aquiiii', rr_count

	rr_file = open('rr_count', 'wb')
	rr_count = rr_file.write(rr_count)
	rr_file.close()

	print rr_count


	return aServer

if len(sys.argv) != 2:
	print 'Modo correto de execução: ./portal X\nonde X: 1=Aleatorio e 2=RoundRobin'
	sys.exit()

rr_count = 0

HOST = ''				# Portal IP
PORT = 5011 			# Portal Port
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
		print 'Recebendo arquivo fonte do Cliente: {}'.format(client)
		aFile = open('./portal_in.txt', 'wb')
		msg = con.recv(1024)
		while msg:
			aFile.write(msg)
			#print client, msg
			if msg[-3:] == 'FIM': 
				aFile.seek(-3, os.SEEK_END)
				aFile.truncate()
				break
			msg = con.recv(1024)
		aFile.close()
		print 'Arquivo fonte recebido com sucesso do Cliente: {}'.format(client)
		# FILE RECEIVED FROM CLIENT

		# CONNECTING TO SERVER
		aServer = connectToServer()
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
			if msg[-3:] == 'FIM':
				aFile.seek(-3, os.SEEK_END)
				aFile.truncate()
				break
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
