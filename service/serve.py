import eventlet
from eventlet.green import socket


PORT = 8080


class Topic(object):
    def __init__(self, name):
        self.name = name
        self.clients = []

    def subscribe(self, client):
        write = client.makefile('w')
        print 'subscribe(%s) %s' % (self.name, write)
        self.clients.append(write)

    def send(self, msg):
        print 'send(%s) %s to %s' % (self.name, msg[:-1], self.clients)
        for c in self.clients:
            try:
                c.write(msg)
                c.flush()
            except socket.error, e:
                if e[0] != 32:  # broken pipe
                    raise
                print 'remove(%s) %s' % (self.name, c)
                self.clients.remove(c)


topics = {}


def myhandle(client, client_addr):
    print "client connected", client_addr

    reader = new_sock.makefile('r')
    line = reader.readline()
    name = line.split(' ')[1].strip()

    if line.startswith('GET /'):
        name = name[1:]
        if not name in topics:
            topics[name] = Topic(name)
        topic = topics[name]
        topic.subscribe(client)
    else:
        if not name in topics:
            topics[name] = Topic(name)
        topic = topics[name]

        line = reader.readline()
        while line:
            topic.send(line)
            line = reader.readline()
        client.close()


server = eventlet.listen(('0.0.0.0', PORT))
pool = eventlet.GreenPool(10000)
while True:
    new_sock, address = server.accept()
    pool.spawn_n(myhandle, new_sock, address)
