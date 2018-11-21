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

UUID=str(uuid.uuid4())

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H','--host', type=str, default='0.0.0.0')
    parser.add_argument('-p','--port', type=int, default=5151)
    result = parser.parse_args()
    return result

def threaded_client(client_list, conn, addr):
    """ Threads single client connections"""
    client_id = "{0}:{1}".format(addr[0],addr[1])

    try:
        client_list.add(client_id)

        while True:

            data = conn.recv(2048)

            if not data:
                break

            elif data.decode('ASCII').strip() == "WHY":
                reply = '42\n'
                conn.sendall(reply.encode('ASCII'))
                print("sent reply to {0}".format(client_id))

            elif data.decode('ASCII').strip() == "WHO":
                reply1 = "client list: {0}\n".format(client_list)
                reply2 = "connected clients: {0}\n".format(str(len(client_list)))
                conn.sendall(reply1.encode('ASCII'))
                conn.sendall(reply2.encode('ASCII'))
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
        conn.close()

def server(host, port, client_list):
    print("starting server...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #setting sockopt so addresses are released after script is killed
    s.bind((host, port))
    s.listen(5)
    while True:
        conn, addr = s.accept()
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
