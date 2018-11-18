import argparse
import socket
import threading
import uuid

UUID=str(uuid.uuid4())

def parse_args():
    """ CLI  """
    parser = argparse.ArgumentParser()
    parser.add_argument('-H','--host', type=str, default='127.0.0.1')
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
                reply1 = "{}\n".format(client_list)
                reply2 = str(len(client_list))
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

            #print(data.encode('ASCII'))

        conn.shutdown(socket.SHUT_RDWR)

    except socket.error as err:
        print("Socket disconnected...")

    finally:
        client_list.remove(client_id)
        conn.close()

def server(host, port, client_list):
    print("Starting server...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        print('connection from: '+addr[0]+':'+str(addr[1]))
        t = threading.Thread(target=threaded_client, args=(client_list, conn, addr))
        t.daemon = True
        t.start()

def main():
    client_list = set() # client must be unique
    args = parse_args()
    try:
        server(args.host, args.port, client_list)
    except KeyboardInterrupt:
        print("Keyboard interrupt")

if __name__ == '__main__':
    main()
