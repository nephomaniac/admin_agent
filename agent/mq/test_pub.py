import zmq
import random
import sys
import time

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)
messagedata = 0
topics = ['config:update:{new_config}:version ', 'event:debug: random message ', 'event:error: agent offline. Missed heartbeats',
          'event:critical: subagent config manager shutting down in ', 'monitoring:cpu: level ']
while True:
    #topic = 'weather'
    if messagedata >= 1000:
        messagedata = 0
    topic = topics[random.randrange(0,5)]
    #messagedata = random.randrange(1,215) - 80
    messagedata += 1
    print "message:{0} {1}".format(topic, messagedata)
    socket.send("%s %d" % (topic, messagedata))
    time.sleep(.1)