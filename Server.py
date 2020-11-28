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
from datetime import datetime


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print ( 'starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)
ThreadCount = 0
#variables del estacionamiento
isOpen = False #estacionamiento abierto o cerrado
parkRequests = 0
removeRequests = 0
parked = 0
removed = 0

#semaforos binario de entradas y salidas
entranceLocks = []
exitLocks = []
getCardLocks = []
laserOffEntLock = []
laserOnEntLock = []
#array de queues
entradas = []
salidas = []
getCardTime = []
getLaserOffEntTime =[]
getLaserOnEntTime = []
#semaforo general de espacios
spaces = None

threadsEntrances = []
threadsExits = []

#variable con el reloj en timepo inicial
baseTime = None

def getCard(num): 
    while True:
        global getCardLocks
        global getCardTime
        getCardLocks[num].acquire()
        newTime = datetime.now()
        clock = newTime - baseTime
        clock = getCardTime[num] - clock.seconds
        print("Comienza a imprimir tarjeta")
        if clock > 0:
            time.sleep(clock)
        newTime = datetime.now()
        print("Se imprimio tarjeta a las ", newTime.strftime("%H:%M:%S"))


def laserOffEnt(num):
    while True:
        global laserOffEntLock
        global getLaserOffEntTime
        laserOffEntLock[num].acquire()
        newTime = datetime.now()
        clock = newTime - baseTime
        clock = getLaserOffEntTime[num] - clock.seconds
        if clock > 0:
            time.sleep(clock)
        print("Auto comienza a pasar")

def laserOnEnt(num):
    while True:
        global laserOffEntLock
        global getLaserOffEntTime
        laserOnEntLock[num].acquire()
        newTime = datetime.now()
        clock = newTime - baseTime
        clock = getLaserOffEntTime[num] - clock.seconds
        if clock > 0:
            time.sleep(clock)
        print("Auto termina de pasar")
        time.sleep(5)
        print("Se bajo la barrera")

def insertCard(num):
	while True:
		global salidas
		carro = salidas[num]
		carro.get()#obtener queue
		exitLocks[num].acquire()
		#seccion critica de la salida
		spaces.release()
		global parked
		parked -= 1
		print('saliendo de la salida: ' + str(num + 1))
		time.sleep(5)
		print("carros dentro: ", parked)
		exitLocks[num].release()
		print('salio!' + str(num + 1))


def pressButton(num):
	while True:
		global entradas
		car = entradas[num]
		car.get() #obtener queue
		entranceLocks[num].acquire()
		#seccion critica de la entrada
		spaces.acquire()
		global parked
		parked += 1
		print('entrando por: ' + str(num + 1))
		time.sleep(5)
		print("carros dentro: ", parked)
		entranceLocks[num].release()
		print('entro! ' + str(num + 1))
		


def apertura(spacesNum, entrancesNum, exitsNum):
	global isOpen
	isOpen = True
	global spaces
	spaces = threading.Semaphore(spacesNum)
	global entradas

	global threadsEntrances
	global threadsExits

	global entranceLocks
	global exitLocks
	global getCardLocks
	global laserOffEntLock
	global laserOnEntLock

	global getCardTime
	global getLaserOffEntTime
	global getLaserOnEntTime

	baseTime = datetime.now()

	oneLock =  threading.Semaphore(1) #semaforo binario para entradas
	zeroLock = threading.Semaphore(0) #semaforo binario para salidas
	
	for i in range(entrancesNum):
		t = threading.Thread(target=pressButton, args=(i,))
		threadsEntrances.append(t)
		entradas.append(queue.Queue(100)) #cada entrada tiene una queue de 100
		getCardTime.append(queue.Queue(100))
		getLaserOffEntTime.append(queue.Queue(100))
		getLaserOnEntTime.append(queue.Queue(100))
		entranceLocks.append(oneLock) #insertar semaforo
		getCardLocks.append(zeroLock)
		laserOffEntLock.append(zeroLock)
		laserOnEntLock.append(zeroLock)
		t.start()

	for i in range(exitsNum):
		t2 = threading.Thread(target=insertCard, args=(i,))
		threadsExits.append(t2)
		salidas.append(queue.Queue(100)) #cada salida tiene una queue de 100
		exitLocks.append(oneLock) #insertar semaforo 
		t2.start()


def runFunc(data):
	values = data.split(" ")
	if "apertura" == values[1]:
		if isOpen:
			print("El estacionamiento ya está abierto.")
		else:
			if len(values) == 5:
				apertura(int(values[2]), int(values[3]), int(values[4]))
			else:
				print("Error en los argumentos!")
	
	if "oprimeBoton" == values[1]:
		if isOpen:
			if len(values) == 3:
				numEnt = int(values[2])
				print("presionando en entrada...", numEnt)
				entradas[numEnt - 1].put(int(values[0]))
			else:
				print("Error en los argumentos!")
		else:
			print("No se ha iniciado el estacionamiento")

	if "meteTarjeta" == values[1]:
		if parked == 0:
			print("No hay autos estacionados!")
			return
		if isOpen:
			if len(values) == 3:
				numSal = int(values[2])
				print("metiendo en salida...", numSal)
				salidas[numSal - 1].put(1)
			else:
				print("Error en los argumentos!")
		else:
			print("No se ha iniciado el estacionamiento")

	if "recogeTarjeta" == values[1]:
		if isOpen:
			if len(values) == 3:
				numEnt = int(values[2])
				print("recogiendo tarjeta...", numEnt)
				getCardTime[numEnt - 1].put(int(values[0]))
			else:
				print("Error en los argumentos!")
		else:
			print("No se ha iniciado el estacionamiento")

	if "laserOffE" == values[1]:
		if isOpen:
			if len(values) == 3:
				numEnt = int(values[2])
				print("recogiendo tarjeta...", numEnt)
				getLaserOffEntTime[numEnt - 1].put(int(values[0]))
			else:
				print("Error en los argumentos!")
		else:
			print("No se ha iniciado el estacionamiento")

	if "laserOnE" == values[1]:
		if isOpen:
			if len(values) == 3:
				numEnt = int(values[2])
				print("recogiendo tarjeta...", numEnt)
				getLaserOnEntTime[numEnt - 1].put(int(values[0]))
			else:
				print("Error en los argumentos!")
		else:
			print("No se ha iniciado el estacionamiento")

	
def multi_threaded_client(connection):
	try:
		print ( 'connection from', client_address)

		while True:   
			data = connection.recv(256)
			print ( 'server received "%s"' % data.decode('utf-8')) # data bytes back to str
			if data:
				connection.sendall(b'va de regreso...' + data) # b converts str to # bytes
				runFunc(str(data.decode('utf-8'))) #funcion principal
			else:
				print ( 'no data from', client_address)
				connection.close()
				break
	finally:
		print ('se fue al finally')
		connection.close()


# Wait for a connection
print ( 'waiting for a connection')

while True:
	connection, client_address = sock.accept()
	t = threading.Thread(target=multi_threaded_client, args=(connection,))
	t.start()
	ThreadCount += 1
	print('Thread Number: ' + str(ThreadCount))
