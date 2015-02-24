import socket
import select

server = socket.socket()
server.bind(('', 9090))
server.listen(1)
input = [server]
data = ''
while data != 'stop':
    inputready,outputready,exceptready = select.select(input,[],[])
    for s in inputready:
        if s == server:
            conn, addr = s.accept()
            input.append(conn)
            print 'Connected new client: ', addr
        else:
            data = s.recv(1024)
            #    break
            if data:
                s.send('Echo: ' + data.upper())
            else:
                print 'Disconnected client'
                s.close()
                input.remove(s)
server.close()
