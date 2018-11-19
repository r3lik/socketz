Socketz
============

A simple TCP server written in Python. It uses HAProxy for Layer 4 load balancing.

Requirements
--------------
* Python 3.0+
* Docker
* Docker Compose

Usage 
------------
* `docker-compose up -d` to provision network, download images and launch containers
* `telnet localhost 4141` to connect to server (roundrobin)

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
python3 server.py                                                                           [13:32:24]
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

To-do
------
* Implement `heartbeat`, `keepalived` or `ucarp` for automatic failover/fault tolerance  
* Implement state handling across the cluster with `etcd` 
