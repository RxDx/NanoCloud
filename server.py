#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import socket
import os
import sys
import subprocess

HOST = ''				# Endereco IP do Servidor
PORT = 4224				# Porta que o Servidor esta
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
while True:
	con, portal = server.accept()
	pid = os.fork()
	if pid == 0:
		server.close()
		print 'Conectado por', portal

		# RECEIVING FILE FROM PORTAL
		print 'Recebendo arquivo fonte do Portal: {}.'.format(portal)
		aFile = open('./server_in.txt', 'wb')
		msg = con.recv(1024)
		while msg:
			aFile.write(msg)
			if msg[-3:] == 'FIM': 
				aFile.seek(-3, os.SEEK_END)
				aFile.truncate()
				break
			if msg != 'FIM': print portal, msg
			msg = con.recv(1024)
		aFile.close()
		print 'Arquivo fonte recebido com sucesso do Portal: {}.'.format(portal)
		# FILE RECEIVED FROM PORTAL

		# EXECUTING FILE
		print 'Executando arquivo fonte.'
		p = subprocess.Popen(["python", "server_in.txt"], stdout=subprocess.PIPE)
		cmdOutput, err = p.communicate()
		print 'Arquivo fonte executado com sucesso.'
		# FILE EXECUTED

		print 'Saída da execução: ', cmdOutput

		# SAVING THE OUTPUT ON A FILE
		print 'Salvando a saída da execução em um arquivo temporário.'
		cFile = open('program_output.txt', 'wb')
		cFile.write(cmdOutput)
		cFile.close()
		print 'Saída da execução salva em um arquivo temporário com sucesso.'
		# OUTPUT SAVED ON A FILE

		# SENDING THE OUTPUT FILE TO PORTAL
		print 'Enviando saída da execução para o Portal: {}.'.format(portal)
		bFile = open('program_output.txt', 'rb')
		msg = bFile.read(1024)
		while msg:
			print 'Enviando saída da execução para o Portal:'+msg;
			con.sendall(msg)
			msg = bFile.read(1024)
		bFile.close()
		con.sendall('FIM')
		print 'Saída da execução enviada com sucesso para o Portal: {}.'.format(portal)
		# OUTPUT SENT TO PORTAL

		print 'Finalizando conexao do cliente', portal
		con.close()
		sys.exit(0)
	else:
		con.close()
