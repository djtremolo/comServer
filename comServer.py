# copypaste from https://pymotw.com/2/select/

import select, socket, sys
#import multiprocessing
import queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind(('localhost', 50000))
server.listen(5)
inputs = [server]
outputs = []
message_queues = {}

pairs = dict()



def pairIsValid(key):
    if (key in pairs):
        print("checking pair %s" % pairs[key])
        if(len(pairs[key])>1):
            return True
    return False



def createPair(sock, key):
    if(key not in pairs):        
        pairs[key] = [sock]
    else:
        if(len(pairs[key]) == 1):
            pairs[key].append(sock)

def removeSocketFromPair(sock, key):
    if(key in pairs):
        if(sock in pairs[key]):
            print("removed %s from pair" % sock)
            pairs[key].remove(sock)
            if(len(pair[key]) == 0):
                print("removed '%s' pair completely" % key)
                del pairs[key]


def forwardMessage(msg, sourceSock, key):
    if(pairIsValid(key)):
        for s in pairs[key]:
            if(s != sourceSock):

                print ('forwarding "%s" from %s to %s' % (msg, sourceSock.getpeername(), s.getpeername()))

                message_queues[s].put(msg)
                if s not in outputs:
                    outputs.append(s)




#def handlePair(newSock)
#    if newsock


while inputs:
    readable, writable, exceptional = select.select(
        inputs, outputs, inputs)
    for s in readable:
        if s is server:
            connection, client_address = s.accept()
            print ('new connection from', client_address)
            connection.setblocking(0)
            inputs.append(connection)
            message_queues[connection] = queue.Queue()

            createPair(connection, "12345678")
#            createPair(connection, "wjkerjhkjwer")
        else:
            data = s.recv(1024)
            if data:
                print ('received "%s" from %s' % (data, s.getpeername()))
                forwardMessage(data, s, "12345678")
#                message_queues[s].put(data)
#                if s not in outputs:
#                    outputs.append(s)
            else:
                print ('closing', client_address, 'after reading no data')

                removeSocketFromPair(s, "12345678")

                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]

    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            outputs.remove(s)
        else:
            s.send(next_msg)

    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]