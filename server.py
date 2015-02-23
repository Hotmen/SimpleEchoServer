import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
data = ''
while data != 'stop':
    conn, addr = sock.accept()

    print 'Connected: ', addr

    while True:
        data = conn.recv(1024)
        if not data or data == 'stop':
            break
        conn.send(data.upper())
    conn.close()