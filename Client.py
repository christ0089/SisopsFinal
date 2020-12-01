#!/usr/bin/env python
# -*- coding: utf-8 -*-

# modificado para python 3.x, mayo 2020
# mayo 14 2008 - corregido para convertir str variable to bytes

# The client program sets up its socket differently from the way a server does. Instead of binding to a port and listening, it uses connect() to attach the socket directly to the remote address.

import socket
import sys
import time
from datetime import datetime

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print ( 'connecting to %s port %s' % server_address)
sock.connect(server_address)


try:
	while True:
		mensaje = input()
		now = datetime.now()
		time = now.strftime("%H:%M:%S")
		# Send data
		if mensaje != 'exit':
			print ( 'client sending "%s"' % mensaje)
			mensaje = time + " " + mensaje
			sock.sendall(mensaje.encode('utf-8'))	
		
			respuesta = sock.recv(256)
			print ( 'client received "%s"' % respuesta.decode('utf-8')) # bytes to string
		else:
			break

finally:
    print ('closing socket')
    sock.close()
	