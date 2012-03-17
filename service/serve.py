import eventlet


class Topic(object):
    def __init__(self):
        self.clients = []

    def subscribe(self, client):
        self.clients.append(client)

    def send(self, msg):
        msg += "\n"
        for c in self.clients:
            c.sendall(msg)


topics = {}


def myhandle(client, client_addr):
    print "client connected", client_addr
    buf = client.recv(1024)
    if buf.startswith('GET /'):
        name = buf.split(' ')[1][1:]
        if not name in topics:
            topics[name] = Topic()
        topic = topics[name]
        topic.subscribe(client)
        print 'SUBSCRIBE %s' % name
    else:
        topic_line = buf.split('\n')[0]
        name = topic_line.split(' ')[1]
        print 'SEND %s' % name
        if not name in topics:
            topics[name] = Topic()
        topic = topics[name]

        # topic.send('hello world')
        # remove the first line from buffer
        buf = buf[buf.index("\n") + 1:]
        topic.send(buf)
        while True:
            buf += client.recv(1)
            while "\n" in buf:
                topic.send(buf[:buf.index("\n")])
                buf = buf[buf.index("\n") + 1:]
            else:
                break
        print 'done?'


server = eventlet.listen(('0.0.0.0', 8080))
pool = eventlet.GreenPool(10000)
while True:
    new_sock, address = server.accept()
    pool.spawn_n(myhandle, new_sock, address)
