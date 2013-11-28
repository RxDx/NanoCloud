#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Fellipe Silveira
# Rodrigo Dumont

import socket
import sys
import os

if len(sys.argv) != 2:
	print 'Modo correto de execução: ./client arquivo'
	sys.exit()
HOST = 'caporal.c3sl.ufpr.br'		# Portal IP
PORT = 5011				# Portal Port

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# SENDING FILE TO PORTAL
print 'Enviando arquivo fonte \'{}\' para o Portal...'.format(sys.argv[1])
aFile = open(sys.argv[1], 'rb')
msg = aFile.read(1024)
while msg:
	client.sendall(msg)
	msg = aFile.read(1024)
aFile.close()
client.sendall('FIM')
print 'Arquivo fonte \'{}\' enviado com sucesso para o Portal.'.format(sys.argv[1])
# FILE SENT TO PORTAL

# RECEIVING REPLY FROM PORTAL
print 'Aguardando resposta do Portal...'
aFile = open('./client_in.txt', 'wb')
msg = client.recv(1024)
while msg:
	aFile.write(msg)
	#print 'Resposta do portal: {}'.format(msg)
	if msg[-3:] == 'FIM': 
		aFile.seek(-3, os.SEEK_END)
		aFile.truncate()
		break
	if msg != 'FIM': print 'Resposta do portal: {}'.format(msg)
	msg = client.recv(1024)
aFile.close()
print 'Resposta do Portal recebida com sucesso.'
# RECEIVED REPLY FROM PORTAL

print 'Conexão encerrada com o Portal.'
client.close()
