Socketz
============

A simple, load balanced TCP server written in Python

Requirements
--------------
* Python 3
* Docker
* Docker Compose

Usage 
------------
* `docker-compose up -d`
* `telnet localhost 4141`

Flags
--------------
* `-H, --host` default `127.0.0.1`
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

