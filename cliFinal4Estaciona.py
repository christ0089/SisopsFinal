#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, sys, time
#
# network initialization
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket
server_address = ('localhost', 10000) 					 # connect socket to port
print ( 'connecting to %s port %s' % server_address)
sock.connect(server_address)                             # ready. Connection established

messages = ['0.00 apertura 2 2 2',   # un estacionamiento pequeño pero con dos entradas y dos salidas...,\
			'1.00 oprimeBoton 1',# entra carro',\
			'1.00 oprimeBoton 1',
			'1.00 oprimeBoton 1',
			'1.00 oprimeBoton 1'
			]
			
			

try:
    globalTime = 0.00
    # Send data
    for m in messages:
        
        timestamp = float(m[0:4])        # timestamp of command
        toSleep = timestamp - globalTime # seconds;
        time.sleep(toSleep)
        globalTime += toSleep
        print ( 'client sending "%s"' % m)
										 # send message to server
        sock.sendall(m.encode('utf-8'))  # a string variable needs to be encoded to utf-8 to convert it to a byte string
        respuesta = sock.recv(256)       # wait for response. El serever solo le manda un ' '
										   
finally:
    print ( 'closing socket')
    sock.close()




def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
