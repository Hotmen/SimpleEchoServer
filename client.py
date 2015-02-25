import socket
import argparse
import sys

def ParseArgs():
    parse = argparse.ArgumentParser(usage='clien.py -s SERVER:PORT -f FILENAME', description='Simple Echo client',
                                    epilog='In interactive mode type help to show available commands')
    parse.add_argument('--server', '-s', type=str, metavar='SERVER:PORT', default='127.0.0.1:9090',
                       help='Address of the server and port to connect (example 192.168.0.1:8080)')
    parse.add_argument('--message', '-m', type=str,default=False,
                       help='Message to send to echo server', required=False)
    parse.add_argument('--file', '-f', type=str, default=False,
                       help='Path to file, that contain data to send to server', required=False)
    return parse.parse_args()

def ClientSocket(args):
    #socket.setdefaulttimeout(3)
    sock = socket.socket()
    address = tuple(args['server'].split(':'))
    try:
        sock.connect((address[0],int(address[1])))
    except socket.error:
        print ('Problem occured with connect to server {}. Check server status.'.format(address))
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
            print 'File reading Error! Check arguments.'
            return

    print 'Welcome to Simple Echo server. Type help for available commands'
    while True:
        sys.stdout.write('>>')
        send = sys.stdin.readline().strip()
        if send == 'help':
            print 'quit : Quit from client app'
            print 'help : Help page'
            continue
        if not send:
            break
        if send == 'quit':
            sys.stdout.write('Good by!')
            sock.close()
            break
        sock.send(send)
        data = sock.recv(1024)
        print data
    sock.close()
    return

if __name__ == '__main__':
    args =  ParseArgs()
    ClientSocket(vars(args))
