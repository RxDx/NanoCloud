#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Fellipe Silveira
# Rodrigo Dumont

import socket
HOST = '127.0.0.1'		# Portal IP
PORT = 5001				# Portal Port

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# SENDING FILE TO PORTAL
print 'Enviando arquivo fonte X para o Portal.'
aFile = open('./client_out.txt', 'rb')
msg = aFile.read(1024)
#while msg:
client.send(msg)
	#msg = aFile.read()
aFile.close()
print 'Arquivo fonte X enviado com sucesso para o Portal.'
# FILE SENT TO PORTAL

# RECEIVING REPLY FROM PORTAL
print 'Aguardando resposta do Portal\n'
aFile = open('./client_in.txt', 'wb')
msg = client.recv(1024)
#while msg:
aFile.write(msg)
print 'A resposta do Portal foi: {} '.format(msg)
#msg = client.recv(1024)
aFile.close()
print 'Resposta do Portal recebida com sucesso '
# RECEIVED REPLY FROM PORTAL

print 'Cliente fecha a conexão com o Portal  '
client.close()