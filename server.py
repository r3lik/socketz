#!/usr/bin/env python3

"""
Created by Mike Czarny on 11/17/2018 as a code challenge for blockchain.com
github.com/r3lik
"""

import argparse
import socket
import threading
import uuid
import etcd3

UUID=str(uuid.uuid4()) # set random UUID for server and convert to string

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H','--host', type=str, default='0.0.0.0')
    parser.add_argument('-p','--port', type=int, default=5151) # internally in the Docker container the port is 5151
    result = parser.parse_args()
    return result


def threaded_client(client_list, conn, addr):
    """ Threads single client connections"""
    client_id = "{0}:{1}".format(addr[0],addr[1]) # address comes from server func

    ETCD_HOST = 'etcd-cluster.socketz.gg' # DNS alias of three ETCD instances. In the "real world", this would be a FQDN that resolves to multiple IPs (roundrobin DNS).
    ETCD_PORT = 2379
    ETCD_CLIENTS_LIST = '/sockets/client_list_cnt'

    etcd = etcd3.client(host=ETCD_HOST,port=ETCD_PORT)

    def clients_increment(key):
        curval = etcd.get(key)[0] #returns tuple
        if curval:
            newval = int(curval.decode('ASCII')) + 1
        else:
            newval = 1
        etcd.put(key,str(newval).encode('ASCII'))
        return

    def clients_decrement(key):
        curval = etcd.get(key)[0]
        if curval:
            newval = int(curval.decode('ASCII')) - 1
        else:
            newval = 0
        etcd.put(key,str(newval).encode('ASCII'))
        return

    def clients_get(key):
        curval = etcd.get(key)[0].decode('ASCII')
        return int(curval)

    try:
        client_list.add(client_id)
        clients_increment(ETCD_CLIENTS_LIST)

        while True:

            data = conn.recv(2048)

            if not data:
                break

            elif data.decode('ASCII').strip() == "WHY":
                reply = '42\n'
                conn.sendall(reply.encode('ASCII'))
                print("sent reply to {0}".format(client_id))

            elif data.decode('ASCII').strip() == "WHO":
                reply1 = "IP:PORT of clients connected to this server: {0}\n".format(client_list) # IP:PORT is of the HAProxy frontend
                reply2 = "clients connected to this server: {0}\n".format(str(len(client_list)))
                reply3 = "clients connected to all servers: {0}\n".format(clients_get(ETCD_CLIENTS_LIST))
                conn.sendall(reply1.encode('ASCII'))
                conn.sendall(reply2.encode('ASCII'))
                conn.sendall(reply3.encode('ASCII'))
                print("sent reply to {0}".format(client_id))

            elif data.decode('ASCII').strip() == "WHERE":
                reply = "{0}\n".format(UUID)
                conn.sendall(reply.encode('ASCII'))
                print("sent reply to {0}".format(client_id))

            elif data.decode('ASCII').strip() == "QUIT":
                break

            else:
                reply = "invalid command:\n use 'WHY', 'WHO', 'WHERE', 'QUIT'\n"
                conn.sendall(reply.encode('ASCII'))

        conn.shutdown(socket.SHUT_RDWR)

    except socket.error as err:
        print("socket disconnected...")

    finally:
        client_list.remove(client_id)
        clients_decrement(ETCD_CLIENTS_LIST)
        conn.close()

def server(host, port, client_list):
    print("starting server...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #setting sockopt so addresses are released after script is killed. Otherwise have to kill PID.
    s.bind((host, port))
    s.listen(5)
    while True:
        conn, addr = s.accept()
       # print(addr) # debugging
        print('connection from: '+addr[0]+':'+str(addr[1]))
        t = threading.Thread(target=threaded_client, daemon = True, args=(client_list, conn, addr)) # daemon thread terminates when main program ends
        t.start()

def main():
    client_list = set() # stores an array of currently connected clients. FOR DEBUGGING. removes client after d/c.
    args = parse_args()
    try:
        server(args.host, args.port, client_list)
    except KeyboardInterrupt:
        print("keyboard interrupt")

if __name__ == '__main__':
    main()
