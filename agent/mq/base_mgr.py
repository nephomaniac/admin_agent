import zmq
import random
import sys
import time
import traceback
import logging


class BaseMgr(object):

    def __init__(self, sub_addrs=None, bootstrap_addr="127.0.0.1:5000", loglevel=10):
        # Dict of addr:port to subscribe to
        self.name = self.__class__.__name__
        self.sub_addrs = sub_addrs or {}
        self.bootstrap_addr = bootstrap_addr or None
        self.subscriptions = {}
        self.publishers = {}
        self._context = None
        self.logger = logging.Logger(self.name, loglevel)

    @property
    def context(self):
        if not self._context:
            self._context = zmq.Context()
        return self._context

    @context.setter
    def context(self, value):
        self._context = value


    def create_subscriber(self, name, port, topicfilter, addr="127.0.0.1"):
        """
        Create subscriber socket. 
        :param port: Integer port to bind to
        :param addr: address string, ie: 127.0.0.1, 1.2.3.4, etc.. Use '*' to bind to all. 
        :return: socket
        """
        port = int(port)
        socket = self.context.socket(zmq.SUB)
        socket.connect("tcp://{0}:{1}".format(addr, port))
        if topicfilter:
            socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
        if not self.subscriptions.get(name, None):
            self.subscriptions[name] = []
        self.subscriptions[name].append(socket)
        return socket

    def create_publisher(self, name, port, addr="127.0.0.1"):
        """
        Create publisher socket. 
        :param port: Integer port to connect to
        :param addr: address string to connect to, ie: 127.0.0.1, localhost, 1.2.3.4, etc.. 
        :return: socket
        """
        port = int(port)
        socket = self.context.socket(zmq.PUB)
        socket.bind("tcp://{0}:{1}".format(addr, port))
        if not self.publishers.get(name, None):
            self.publishers[name] = []
        self.publishers[name].append(socket)
        return socket


    def close_all_sockets(self):
        errors = []
        for name, sub in self.subscriptions.iteritems():
            try:
                sub.close()
            except Exception as E:
                self.logger.exception('Error closing {0} subscriber socket:'.format(name))
                errors.append(E)
        for name, pub in self.publishers.iteritems():
            try:
                pub.close()
            except Exception as E:
                self.logger.exception('Error closing {0} publisher socket:'.format(name))
                errors.append(E)
        if errors:
            err_msg = '"{0}" Errors during socket teardown...\n'.format(len(errors))
            for error in errors:
                err_msg += "{0}\n".format(error)
            self.logger.error(err_msg)
            raise RuntimeError(err_msg)

    def get_config(self):
        pass

    def run(self):
        while True:




while True:
    topic = random.randrange(9999, 10005)
    messagedata = random.randrange(1, 215) - 80
    print "%d %d" % (topic, messagedata)
    socket.send("%d %d" % (topic, messagedata))
    time.sleep(1)


#Subscriber
port = "5556"
if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)

if len(sys.argv) > 2:
    port1 = sys.argv[2]
    int(port1)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print "Collecting updates from weather server..."
socket.connect("tcp://localhost:%s" % port)

if len(sys.argv) > 2:
    socket.connect("tcp://localhost:%s" % port1)

# Subscribe to zipcode, default is NYC, 10001
topicfilter = "10001"
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

# Process 5 updates
total_value = 0
for update_nbr in range(5):
    string = socket.recv()
    topic, messagedata = string.split()
    total_value += int(messagedata)
    print topic, messagedata

print "Average messagedata value for topic '%s' was %dF" % (topicfilter, total_value / update_nbr)

