import socket
import argparse
import sys


def parsargs():
    parse = argparse.ArgumentParser(usage='client.py -s SERVER:PORT -f FILENAME', description='Simple Echo client',
                                    epilog='In interactive mode type help to show available commands')
    parse.add_argument('--server', '-s', type=str, metavar='SERVER:PORT', default='127.0.0.1:9090',
                       help='Address of the server and port to connect (example 192.168.0.1:8080)')
    parse.add_argument('--message', '-m', type=str, default=False,
                       help='Message to send to echo server', required=False)
    parse.add_argument('--file', '-f', type=str, default=False,
                       help='Path to file, that contain data to send to server', required=False)
    return parse.parse_args()


def clientsocket(args):
    sock = socket.socket()
    address = tuple(args['server'].split(':'))
    try:
        sock.connect((address[0], int(address[1])))
    except socket.error:
        sys.stdout.write('Problem occurred with connect to server {}. Check server status.'.format(address))
        return

    sys.stdout.write('Trying to connect...\n')
    try:
        sock.send(' ')
        sock.settimeout(60)
        sock.recv(1024)
        sys.stdout.write('Welcome to Simple Echo server. Type help for available commands\n')
        sys.stdout.write('Ready to receive messages\n')
    except socket.timeout:
            sys.stdout.write('Server is full or busy, try later!')
            sock.close()
            return

    if args['message']:
        sock.send(args['message'])
        print sock.recv(1024)
        sock.close()
        return

    if args['file']:
        try:
            datafile = open(args['file'])
            data = datafile.read()
            sock.send(data)
            print sock.recv(1024)
            datafile.close()
            sock.close()
            return
        except:
            sys.stdout.write('File reading Error! Check arguments.\n')
            return

    while True:
        sys.stdout.write('>>')
        send = sys.stdin.readline().strip()
        if send == 'help':
            sys.stdout.write('quit : Quit from client app\n')
            sys.stdout.write('help : Help page\n')
            continue
        if send == 'quit' or not send:
            sys.stdout.write('Good by!')
            sock.close()
            break
        if send == 'stop':
            sock.send(send)
            sys.stdout.write('Good by!')
            sock.close()
            break
        sock.send(send)
        data = sock.recv(1024)
        sys.stdout.write(data+'\n')
    sock.close()
    return

if __name__ == '__main__':
    arguments = parsargs()
    clientsocket(vars(arguments))