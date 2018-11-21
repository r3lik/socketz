Socketz
============
![socket](https://github.com/r3lik/socketz/blob/master/socket.png)

A simple TCP server written in Python. It uses HAProxy for Layer 4 load balancing/HA and ETCD for state replication.

![screencap](https://github.com/r3lik/socketz/blob/master/socket.gif)

Requirements
--------------
* Python 3.0+
* Docker
* Docker Compose

Usage
------------
* `docker-compose up -d` to provision network, download images and launch containers
* `telnet localhost 4141` to connect to server (roundrobin)
* `docker kill server01` to demonstrate that new requests roundrobin to healthy servers only
* `docker exec etcd01 /bin/sh -c "export ETCDCTL_API=3 && /usr/local/bin/etcdctl member list"` to list nodes in cluster


HAProxy stats
-------------
* `http://localhost:9000/stats` admin:hodl

Commands
-------------
* `WHO` outputs the total number of clients connected and their IP:port for debugging
  - with `etcd` this will output the total number of clients connected to all available servers
* `WHERE` outputs the id of the server (unique identifier)
* `WHY` outputs the string "42" ;]
* `QUIT` terminates session :wave:

Flags
--------------
* `-H, --host` default `0.0.0.0`
* `-p, --port` default `5151`

Debugging
-------------
* `docker-compose config` prints out config with var substitution
* `docker-compose ps` lists running containers launched
* `docker attach <name>` attaches to tty

Sample ouput: server
----------------

```
python3 server.py
Starting server...
connection from: 127.0.0.1:61623
sent reply to 127.0.0.1:61623
sent reply to 127.0.0.1:61623
sent reply to 127.0.0.1:61623
sent reply to 127.0.0.1:61623
```

Sample output: client
---------------

```
telnet 127.0.0.1 6000
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
use 'WHY', 'WHO', 'WHERE', 'QUIT'
WHO
client list: {'127.0.0.1:50814', '127.0.0.1:50812'}
connected clients: 2
WHERE
69bbfcac-0fc2-48d4-ba23-4eb100dc925d
```

State replication
-----------------
We can implement state replication of connected clients across the cluster with `etcd`. To add fault tolerance, it's recommended to run an odd number of nodes in the cluster e.g. 5. The python `requests` or `etcd3` library can be used to add/remove connected clients using the `etcd` api. The K/V store would become the source of truth for all three of the backend servers, and our server command `WHO` would list all connected clients on all available server backends. This would replace the existing set that is currently unaware of another servers' state. Consistency would be enforced by `Raft`, the consensus algorithm used by `etcd`.


```
❯ docker exec etcd01 /bin/sh -c "export ETCDCTL_API=3 && /usr/local/bin/etcdctl put clients 5"`
OK

❯ docker exec etcd02 /bin/sh -c "export ETCDCTL_API=3 && /usr/local/bin/etcdctl get clients"
clients
5

❯ docker exec etcd03 /bin/sh -c "export ETCDCTL_API=3 && /usr/local/bin/etcdctl get clients"
clients
5
```
This shows that a key:value pair put on `etcd01` is made available to `etcd02` and `etcd03` via the `Raft` consensus algorithm.
In the server code, I would add a function to increment/decrement the `clients` value based on connections/disconnections.
