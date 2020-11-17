#!/usr/bin/env python
# -*- coding: utf-8 -*-

#modified for python 3.x may 2020
#modified 14 may to convert/deconvert str to bytes

#This sample program, based on the one in the standard library documentation, receives incoming messages and echos them back to the sender. It starts by creating a TCP/IP socket.

import socket
import sys
import time
import threading

threads = []

entrances = None
exits = None
spaces = None

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Then bind() is used to associate the socket with the server address. In this case, the address is localhost, referring to the current server, and the port number is 10000.

# Bind the socket to the port
server_address = ('localhost', 10000)
print ( 'starting up on %s port %s' % server_address)
sock.bind(server_address)

#Calling listen() puts the socket into server mode, and accept() waits for an incoming connection.

# Listen for incoming connections
sock.listen(1)

# Wait for a connection
print ( 'waiting for a connection')
connection, client_address = sock.accept()

#accept() returns an open connection between the server and client, along with the address of the client. The connection is actually a different socket on another port (assigned by the kernel). Data is read from the connection with recv() and transmitted with sendall().

try:
	print ( 'connection from', client_address)

    # Receive the data 
	while True:   
		data = connection.recv(256)
		print ( 'server received "%s"' % data.decode('utf-8')) # data bytes back to str
		if data:
			# print ( 'sending answer back to the client')
			runFunc(data)
			connection.sendall(b'va de regreso...' + data) # b converts str to
                                                                                                                # bytes
		else:
			print ( 'no data from', client_address)
			connection.close()
			sys.exit()
			
finally:
     # Clean up the connection
	print ( 'se fue al finally')
	connection.close()

#When communication with a client is finished, the connection needs to be cleaned up using close(). This example uses a try:finally block to ensure that close() is always called, even in the event of an error.

def worker(num):
	"""thread worker function"""
	print ('Worker: %s' % num)
	return
	
def initWorkers(num):
    
    return 

def apertura(entrancesNum, exitsNum, spacesNum):
	global threadsEntrances
	global entrances
	entrances = []
	for i in range(entrancesNum):
		t = threading.Thread(target=pressButton, args=(i,))
		threadsEntrances.append(t)
		t.start()
		hold = thread.Semaphore(1)
		entrances.append(hold)
	
	global threadsExits
	global exits
	exits = []
	for i in range(exitsNum):
		t = threading.Thread(target=worker, args=(i,))
		threadsExits.append(t)
		t.start()
		hold = thread.Semaphore(1)
		exits.append(hold)
	
	global spaces
	spaces = threading.Semaphore(spacesNum)
	return ""
	
def pressButton(num):
	
	return ""
	
def lasserOnE():
	
	return ""
	
def lasserOffE():
	
	return ""
	
def lasserOnS():
	
	return ""
	
def lasserOffS():
	
	return ""




def pickCards():
	return ""

def putCards():
	return ""



def close():
	return 

def runFunc(data, args = 0):
	values = data.split(" ")
	switcher = {
		"Apertura" : apertura,
		"Cierre" : close,
		"Meter Tarjeta" : putCards,
		"RecogeTarjeta": pickCards,
		"LaserOnE": 5,
		"LaserOffE": 6,
		"OprimeBoton": pressButton,
		"LaserOffS": 9,
		"LaserOnS": 10
	}

	func = switcher.get(values[0], lambda: "Invalid Input")
	func()

#Hello

