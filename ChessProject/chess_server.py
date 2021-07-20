import socket
import pickle

s = socket.socket()
port = 12345
s.bind(('127.0.0.1', port))
s.listen(5)
a = {"dvir":"1234","yonatan":"3434","shalom":"6767"}
c, addr = s.accept()
sendData = "Enter usrename:"
c.send(sendData.encode())
while True:
    rcvdData = c.recv(1024).decode()
    print( "S:",rcvdData)
    if rcvdData in a :
        sendData = "graet now wait!"
        c.send(sendData.encode())
    else :
        sendData = "try again!"
        c.send(sendData.encode())
    if(rcvdData == "Bye" or rcvdData == "bye"):
        break
c.close()