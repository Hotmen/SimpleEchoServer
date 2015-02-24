import socket
sock = socket.socket()
sock.connect(('localhost', 9090))
print 'Welcome to Simple Echo server. Type help for avialable commands'
while True:
    #sock.connect(('localhost', 9090))
    send = raw_input('>>')
    if send == 'help':
        print 'quit : Quit from client app'
        print 'stop : Stop server and client apps'
        print 'help : Help page'
        continue
    if send == 'stop':
        sock.send(send)
        sock.close()
        break
    if send == 'quit':
        #sock.send(send)
        #data = sock.recv(1024)
        sock.close()
        break
    sock.send(send)
    data = sock.recv(1024)
    print data
sock.close()
