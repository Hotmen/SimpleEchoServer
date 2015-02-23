import socket
sock = socket.socket()
sock.connect(('localhost', 9090))
while True:
    send = raw_input('Enter message: ')
    if send == 'stop':
        sock.send(send)
        sock.close()
        break
    if send == 'quit':
        sock.send(send)
        data = sock.recv(1024)
        sock.close()
        break
    sock.send(send)
    data = sock.recv(1024)
    print data
sock.close()
