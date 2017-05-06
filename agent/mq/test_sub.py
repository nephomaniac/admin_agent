import sys
import zmq
import time

max_messages = 25
topics = ['config:update', 'event:critical', 'monitoring:cpu']

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

print "Collecting {0} updates about weather and sports from server...".format(max_messages)
socket.connect("tcp://localhost:%s" % port)

if len(sys.argv) > 2:
    socket.connect("tcp://localhost:%s" % port1)

# Subscribe to topics
topicdata = {}
for topic in topics:
    socket.setsockopt(zmq.SUBSCRIBE, topic)
    topic, topic_type = topic.split(':')
    topicdata[topic] = {}
    topicdata[topic][topic_type] = []

start = time.time()
msgcnt = 0
for update_nbr in range(max_messages):
    msgcnt += 1
    msg = socket.recv()
    msplit = msg.split(':')
    topic = msplit[0]
    t_type = msplit[1]
    data = msg[len(topic): -1]

    topicdata[topic][t_type].append(data)
    print "msg#{0}/{1}, topic:{2}, sub-type:{3}, data:{4}"\
        .format(msgcnt, max_messages, topic, t_type, data)
elapsed = int(time.time() - start)

print "\n*** Collected {0} messages over {1} seconds ***".format(max_messages, elapsed)
for category, subcat in topicdata.iteritems():
    count = 0
    avg_time = 0
    subtype = None
    for subtype, values in subcat.iteritems():
        count = len(values)
        avg_time = float(float(count) / float(elapsed))
    print "Topic filter: {0}, sub-type: {1},  items: {2}, rate: {3:.2f} msg/second "\
        .format(str(category).ljust(15), str(subtype).ljust(15), count, avg_time)

