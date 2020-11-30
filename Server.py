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
laserOffSalLock = []
laserOnSalLock = []

#array de queues
entradas = []
salidas = []
getCardTime = []
getLaserOffEntTime =[]
getLaserOnEntTime = []
getLaserOffSalTime = []
getLaserOnSalTime = []

#semaforo general de espacios
spaces = None

threadsEntrances = []
threadsExits = []
threadsGetCards = []
threadsLaserOffEnt = []
threadsLaserOnEnt = []

threadsLaserOffSal = []
threadsLaserOnSal = []
#variable con el reloj en timepo inicial
baseTime = datetime.now()

#
# Funciones de entrada
#

def pressButton(num):
	global entradas
	global entranceLocks
	global getCardLocks
	while True:
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
		getCardLocks[num].release()
		print('entro! ' + str(num + 1))


def getCard(num): 
	global getCardLocks
	global getCardTime
	global laserOffEntLock
	global baseTime
	while True:
		getCardLocks[num].acquire()
		newTime = datetime.now()
		clock = newTime - baseTime
		clock = getCardTime[num].get() - clock.seconds
		print("Comienza a imprimir tarjeta")
		if clock > 0:
			time.sleep(clock)
		newTime = datetime.now()
		print("Se imprimio tarjeta a las ", newTime.strftime("%H:%M:%S"))
		laserOffEntLock[num].release()


def laserOffEnt(num):
	global laserOffEntLock
	global getLaserOffEntTime
	global laserOnEntLock
	global baseTime
	while True:
		laserOffEntLock[num].acquire()
		newTime = datetime.now()
		clock = newTime - baseTime
		clock = getLaserOffEntTime[num].get() - clock.seconds
		if clock > 0:
			time.sleep(clock)
		print("Auto comienza a pasar")
		laserOnEntLock[num].release()

def laserOnEnt(num):
	global laserOffEntLock
	global getLaserOffEntTime
	global getCardLocks
	global baseTime
	while True:
		laserOnEntLock[num].acquire()
		newTime = datetime.now()
		clock = newTime - baseTime
		clock = getLaserOnEntTime[num].get() - clock.seconds
		if clock > 0:
			time.sleep(clock)
		print("Auto termina de pasar")
		time.sleep(5)
		print("Se bajo la barrera")
		getCardLocks[num].release()
        
# 
#	Funciones de salidas
#

def laserOffSal(num):
	global laserOffSalLock
	global getLaserOffSalTime
	global laserOnSalLock
	while True:
		laserOffSalLock[num].acquire()
		newTime = datetime.now()
		clock = newTime - baseTime
		clock = getLaserOffSalTime[num].get() - clock.seconds
		if clock > 0:
			time.sleep(clock)
		print('Comienza carro salida ' + str(num))
		laserOnSalLock[num].release()
		

def laserOnSal(num):
	global laserOnSalLock
	global getLaserOnSalTime
	global exitLocks
	while True:
		laserOnSalLock[num].acquire()
		newTime = datetime.now()
		clock = newTime - baseTime
		clock = getLaserOnSalTime[num].get() - clock.seconds
		if clock > 0:
			time.sleep(clock)
		print('Sale carro salida ' + str(num))
		exitLocks[num].release()
		

def insertCard(num):
	global salidas
	global exitLocks
	global laserOffSalLock
	while True:
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
		laserOffSalLock[num].release()
		print('salio!' + str(num + 1))
		

def cierre(): 
	global isOpen
	isOpen = False
	print('Se cierra el estacionamineto')


def apertura(spacesNum, entrancesNum, exitsNum):
	global isOpen
	isOpen = True
	global spaces
	spaces = threading.Semaphore(spacesNum)
	global entradas

	global threadsEntrances
	global threadsExits
	global threadsGetCards
	global threadsLaserOffEnt
	global threadsLaserOnEnt
	global threadsLaserOffSal
	global threadsLaserOnSal

	global entranceLocks
	global exitLocks
	global getCardLocks
	global laserOffEntLock
	global laserOnEntLock
	global laserOffSalLock
	global laserOnSalLock

	global getCardTime
	global getLaserOffEntTime
	global getLaserOnEntTime
	global getLaserOffSalTime
	global getLaserOnSalTime

	baseTime = datetime.now()

	for i in range(entrancesNum):
		t = threading.Thread(target=pressButton, args=(i,))
		threadsEntrances.append(t)
		t1 = threading.Thread(target=getCard, args=(i,))
		threadsGetCards.append(t1)
		t2 = threading.Thread(target=laserOffEnt, args=(i,))
		threadsLaserOffEnt.append(t2)
		t3 = threading.Thread(target=laserOnEnt, args=(i,))
		threadsLaserOnEnt.append(t3)
		
		entradas.append(queue.Queue(100)) #cada entrada tiene una queue de 100
		getCardTime.append(queue.Queue(100))
		getLaserOffEntTime.append(queue.Queue(100))
		getLaserOnEntTime.append(queue.Queue(100))
		
		entranceLocks.append(threading.Semaphore(1)) #insertar semaforo
		getCardLocks.append(threading.Semaphore(0))
		laserOffEntLock.append(threading.Semaphore(0))
		laserOnEntLock.append(threading.Semaphore(0))
		t.start()
		t1.start()
		t2.start()
		t3.start()
		

	for i in range(exitsNum):
		t4 = threading.Thread(target=insertCard, args=(i,))
		threadsExits.append(t4)
		t5 = threading.Thread(target=laserOffSal, args=(i,))
		threadsLaserOffSal.append(t5)
		t6 = threading.Thread(target=laserOnSal, args=(i,))
		threadsLaserOnEnt.append(t6)
		
		salidas.append(queue.Queue(100)) #cada salida tiene una queue de 100
		getLaserOffSalTime.append(queue.Queue(100))
		getLaserOnSalTime.append(queue.Queue(100))
		
		exitLocks.append(threading.Semaphore(1)) #insertar semaforo 
		laserOffSalLock.append(threading.Semaphore(0))
		laserOnSalLock.append(threading.Semaphore(0))
		t4.start()
		t5.start()
		t6.start()


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
		print('en oprime boton ' + str(len(values)))
		if isOpen:
			if len(values) == 3:
				numEnt = int(values[2])
				print("presionando en entrada...", numEnt)
				entradas[numEnt - 1].put(float(values[0]))
			else:
				print("Error en los argumentos!")
		else:
			print("No se ha iniciado el estacionamiento")

	if "meteTarjeta" == values[1]:
		if parked == 0:
			print("No hay autos estacionados!")
			return
		if isOpen:
			if len(values) == 5:
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
				getCardTime[numEnt - 1].put(float(values[0]))
			else:
				print("Error en los argumentos!")
		else:
			print("No se ha iniciado el estacionamiento")

	if "laserOffE" == values[1]:
		if isOpen:
			if len(values) == 3:
				numEnt = int(values[2])
				print("Apagando laser de entrada...", numEnt)
				getLaserOffEntTime[numEnt - 1].put(float(values[0]))
			else:
				print("Error en los argumentos!")
		else:
			print("No se ha iniciado el estacionamiento")

	if "laserOnE" == values[1]:
		if isOpen:
			if len(values) == 3:
				numEnt = int(values[2])
				print("Prendiendo laser de entrada...", numEnt)
				getLaserOnEntTime[numEnt - 1].put(float(values[0]))
			else:
				print("Error en los argumentos!")
		else:
			print("No se ha iniciado el estacionamiento")

	if "laserOffS" == values[1]:
		if isOpen:
			if len(values) == 3:
				numEnt = int(values[2])
				print("Apagando laser de salida...", numEnt)
				getLaserOffSalTime[numEnt - 1].put(float(values[0]))
			else:
				print("Error en los argumentos!")
		else:
			print("No se ha iniciado el estacionamiento")

	if "laserOnS" == values[1]:
			if isOpen:
				if len(values) == 3:
					numEnt = int(values[2])
					print("Prendiendo laser de salida...", numEnt)
					getLaserOnSalTime[numEnt - 1].put(float(values[0]))
				else:
					print("Error en los argumentos!")
			else:
				print("No se ha iniciado el estacionamiento")
	if "cierre" == values[1]:
		if isOpen:
			cierre()
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
