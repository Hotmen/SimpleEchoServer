import socket
import threading
import logging
import sys
import Queue
import time
import argparse
logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s',)


def parseargs():
    parse = argparse.ArgumentParser(usage='server.py -p PORT -q NUMBER_OF PROCESS', description='Simple Echo server',
                                    epilog='End of description')
    parse.add_argument('--port', '-p', type=str, metavar='PORT', default='9090',
                       help='Port to connection (default 9090)')
    parse.add_argument('--queue', '-q', type=str, metavar='NUMBER', default=2,
                       help='Number of active threads (default 2)')
    return parse.parse_args()


class Server:
    def __init__(self, arg):
        self.logger = logging.getLogger('Server')
        self.logger.debug('Init server')
        self.host = 'localhost'
        self.port = int(arg['port'])
        self.backlog = 1
        self.buffsize = 1024
        self.server = None
        self.threads = []
        self.queue = Queue.Queue()
        self.workers = int(arg['queue'])

    def open_socket(self):
        try:
            self.server = socket.socket()
            self.logger.debug('Create new socket')
            self.server.bind((self.host, self.port))
            self.server.listen(self.backlog)
            self.logger.debug('Listen new socket')
        except:
            self.logger.debug('Error while open socket')
            sys.exit()

    def run(self):
        self.open_socket()
        self.logger.debug('Start running')
        for i in range(self.workers):
            cl = Client(self.queue)
            cl.start()
        while True:
            self.queue.put(self.server.accept())
            self.logger.debug('New object added in queue')
        self.server.close()


class Client(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(self.name)
        self.logger.debug('init new thread')
        self.daemon = True
        self.queue = q
    def run(self):
        while True:
            client, addr = self.queue.get()
            self.logger.debug('New connection from {}'.format(addr))
            self.logger.debug('Processing by Thread ID - {}'.format(self.ident))
            start = time.time()
            while True:
                try:
                    data = client.recv(1204)
                    if data:
                        client.send('Echo: ' + data.upper())
                    else:
                        self.logger.debug('Disconnected {}'.format(addr))
                        client.close()
                        break
                except socket.error:
                    self.logger.debug('Disconnected {}'.format(addr))
                    break

            diff = time.time() - start
            self.logger.debug('Task done. Working time: %.2f seconds'%(diff))
            self.queue.task_done()

if __name__ == '__main__':
    arg = parseargs()
    ser = Server(vars(arg))
    ser.run()