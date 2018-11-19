Socketz 
============
![socket](https://github.com/r3lik/socketz/blob/master/socket.png)

A simple TCP server written in Python. It uses HAProxy for Layer 4 load balancing and HA. 

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

HAProxy stats
-------------
* `http://localhost:9000/stats` admin:hodl  

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
To achieve this, we can implement state persistence of connected clients across the cluster with `etcd`. To add fault tolerance, we would run multiple instances/containers of the k/v store behind `HAProxy`. The python `requests` library can be used to update/remove connected clients using the `etcd` api. This would replace the existing set that is unaware of another servers' state.  
