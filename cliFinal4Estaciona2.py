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

messages = ['0.00 apertura 2 2 2',
			'1.00 oprimeBoton 1',
			'8.00 recogeTarjeta 1',
			'15.00 laserOffE 1',
			'17.00 laserOnE 1',
			'27.00 meteTarjeta 1 1 22.0',
			'35.00 laserOffS 1',
			'37.00 laserOnS 1',
			'44.00 oprimeBoton 1',
			'44.00 oprimeBoton 2',
			'51.00 recogeTarjeta 1',
			'51.00 recogeTarjeta 2',
			'58.00 laserOffE 1',
			'58.00 laserOffE 2',
			'59.00 laserOnE 1',
			'59.00 laserOnE 2',
			'66.00 oprimeBoton 1',
			'71.00 oprimeBoton 1',
			'73.00 meteTarjeta 1 1 66.0',
			'80.00 laserOffS 1',
			'81.00 laserOnS 1',
			'82.00 oprimeBoton 1',
			'89.00 recogeTarjeta 1',
			'95.00 laserOffE 1',
			'96.00 laserOnE 1',
			'97.00 meteTarjeta 1 1 83.0',
			'103.00 laserOffS 1',
			'104.00 laserOnS 1',
			'110.00 meteTarjeta 2',
			'128.00 meteTarjeta 2 1 112.00',
			'132.00 meteTarjeta 2 1 130.00',
			'139.00 laserOffS 1',
			'140.00 laserOnS 1',
			'140.00 cierre'         ]
			
			
			 
           

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
