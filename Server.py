#!/usr/bin/env python
# -*- coding: utf-8 -*-

#modified for python 3.x may 2020
#modified 14 may to convert/deconvert str to bytes

#This sample program, based on the one in the standard library documentation, receives incoming messages and echos them back to the sender. It starts by creating a TCP/IP socket.

import socket
import sys
import time
import threading
import queue

entrances = []
exits = []
spaces = None
threadsEntrances = []
threadsExits = []

def worker(num):
    
    return 
	
def pressButton(num):
	while True:	
		print(str(num))
		global entrances
		car = entrances[num].get()
		print ( 'inside ' + str(num))
		time.sleep(3)
		print ( 'outside ' + str(num))
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
	
def apertura(spacesNum, entrancesNum, exitsNum):
	print ( 'apertura')
	global threadsEntrances
	global entrances
	entrances = []
	for i in range(entrancesNum):
		t = threading.Thread(target=pressButton, args=(i,))
		threadsEntrances.append(t)
		t.start()
		hold = queue.Queue(100)
		entrances.append(hold)
	
	global threadsExits
	global exits
	exits = []
	for i in range(exitsNum):
		t = threading.Thread(target=worker, args=(i,))
		threadsExits.append(t)
		t.start()
		hold = queue.Queue(100)
		exits.append(hold)
	
	global spaces
	spaces = threading.Semaphore(spacesNum)
	return ""
	
def runFunc(data):
	values = data.split(" ")
	
	if "apertura" == values[1]: 
		apertura(int(values[2]), int(values[3]), int(values[4]))

	if "oprimeBoton" == values[1]:
		entrances[int(values[2])-1].put(1)
		
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
		data = data.decode('utf-8')
		if data:
			print ( 'server received "%s"' % data) # data bytes back to str
			runFunc(data)
			data += " va de regreso..."
			connection.sendall(data.encode('utf-8'))
                                                                                                                # bytes
                                                                                                                
		else:
			break
			
finally:
    # Clean up the connection
	time.sleep(2)
	print ( 'se fue al finally')
	connection.close()

#When communication with a client is finished, the connection needs to be cleaned up using close(). This example uses a try:finally block to ensure that close() is always called, even in the event of an error.

def worker(num):
	"""thread worker function"""
	print ('Worker: %s' % num)
	return
	



#Hello

