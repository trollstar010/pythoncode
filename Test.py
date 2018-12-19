import time
import serial
import socket
from firebase import firebase

usbport = 'COM4'
ser = serial.Serial(usbport, 9600, timeout=1)
firebase = firebase.FirebaseApplication('https://assistant-221622.firebaseio.com')
print('online')


host = '192.168.0.28'
port = '10003'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.28",10003))

while True:
    result = firebase.get('/drink',None)
    
    if (result == 'water' ):
        command = 'MoveHoming,0,;'
        x = 180
        print ('serving water')
        s.send(str.encode(command))
        ser.write(str(x).encode())
        reply = s.recv(1024)
        print(reply.decode('utf-8'))
        while (result=='water'):
            result = firebase.get('/drink',None)
            if (result!='water'):
                x=0
                ser.write(str(x).encode())
                print('exit water')
                break

        
    elif (result == 'coke' ):
        mode='SetRunningMode,1,;'
        command = 'F_hi,;'
        print ('serving coke')
        s.send(str.encode(mode))
        s.send(str.encode(command))
        reply = s.recv(1024)
        print(reply.decode('utf-8'))
        while (result=='coke'):
            result = firebase.get('/drink',None)
            if (result!='coke'):
                mode='SetRunningMode,0,;'
                s.send(str.encode(mode))
                print('exit coke')
                break
        
    elif (result == 'coffee' ):
        command = 'MoveJ,0,-90,0,0,0,0,60,;'
        print ('serving coffee')
        s.send(str.encode(command))
        reply = s.recv(1024)
        print(reply.decode('utf-8'))
        while (result=='coffee'):
            result = firebase.get('/drink',None)
            if (result!='coffee'):
                print('exit coffee')
                break

    elif (result == 'sprite' ):
        mode='SetRunningMode,1,;'
        command = 'F_close,;'
        x=180
        ser.write(str(x).encode())
        print ('serving sprte')
        s.send(str.encode(mode))
        s.send(str.encode(command))
        time.sleep(3)
        x=0
        ser.write(str(x).encode())
        reply = s.recv(1024)
        print(reply.decode('utf-8'))
        
        while (result=='sprite'):
            result = firebase.get('/drink',None)
            if (result!='sprite'):
                mode='SetRunningMode,0,;'
                s.send(str.encode(mode))
                print('exit sprite')
                break
        
    elif result == 'KILL' :
        #send KILL command
        s.send(str.encode(command))
        reply = s.recv(1024)
        print(reply.decode('utf-8'))
        break


s.close()
