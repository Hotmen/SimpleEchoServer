import socket
import threading
import logging
import sys
#import multiprocessing
logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s',)

class Server:
    def __init__(self, port):
        self.logger = logging.getLogger('Server')
        self.logger.debug('init')
        self.host = 'localhost'
        self.port = port
        self.backlog = 1
        self.buffsize = 1024
        self.server = None
        self.threads = []
        self.queue = []

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

    def handler(self, clientsock, addr):
        self.logger.debug('New connection from {}'.format(addr))
        while True:
            try:
                data = clientsock.recv(self.buffsize)
                if data:
                    self.logger.debug('Recive data - {}'.format(data))
                    clientsock.send('Echo: ' + data.upper())
                else:
                    self.logger.debug('Disconnected client')
                    clientsock.close()
                    #thread.exit()
                    return
            except socket.error:
                self.logger.debug('Error! Maybe client is disconnected')
                return
    def start_conn(self, sock):
        worker = threading.Thread(target=self.server_client, args=(sock,))
        worker.deamon = True
        worker.start()

    def server_client(self, sock):
        clientsock, addr = sock.accept()
        while True:
            try:
                data = clientsock.recv(self.buffsize)
                if data:
                    self.logger.debug('Recive data - {}'.format(data))
                    clientsock.send('Echo: ' + data.upper())
                else:
                    self.logger.debug('Disconnected client')
                    clientsock.close()
                    #thread.exit()
                    return
            except socket.error:
                self.logger.debug('Error! Maybe client is disconnected')
                return

    def run(self):
        self.open_socket()
        self.logger.debug('Start running')
        workers = []
        for i in range(2):
            workers.append(self.start_conn(self.server))
        while True:
            #self.logger.debug('Waiting for connection ....')
            for worker in self.threads:
                if not worker.isAlive():
                    self.threads.remove(worker)
                    self.threads.append(self.start_conn(self.server))
            #cl = Client(self.server.accept())
            #if len(self.threads) > 2:
            #    self.logger.debug('To many connections! New client add in queue.')
            #    self.queue.append(cl)
            #else:
            #cl.start()
            #self.threads.append(cl)
            #for th in self.threads:
            #    if not th.isAlive():
            #        self.threads.remove(th)
            #        waitconn = self.queue.pop()
            #        waitconn.start()
            #        self.threads.append(waitconn)
            #self.logger.debug('Number of threads {}'.format(len(self.threads)))
        self.server.close()
        for c in self.threads:
            c.join()

class Client(threading.Thread):
    def __init__(self, (client, addr)):
        self.logger = logging.getLogger('Client')
        self.logger.debug('init')
        threading.Thread.__init__(self)
        self.client = client
        self.address = addr
        self.logger.debug('New connection from {}'.format(self.address))
    def run(self):
        while True:
            try:
                data = self.client.recv(1204)
                if data:
                    self.logger.debug('Reciving - {}'.format(data))
                    self.client.send('Echo: ' + data.upper())
                else:
                    self.logger.debug('Disconnected')
                    self.client.close()
                    return
            except socket.error:
                return

if __name__ == '__main__':
    ser = Server(9090)
    ser.run()
