Socketz
============

A simple TCP server written in Python

Requirements
--------------
Python 3

Flags
--------------
* `-H, --host` default `127.0.0.1`
* `-p, --port` default `5151`

Sample: Server 
----------------

```
python3 server.py -p 6000                                                                           [13:32:24]
Starting server...
connection from: 127.0.0.1:61623
sent reply to 127.0.0.1:61623
sent reply to 127.0.0.1:61623
sent reply to 127.0.0.1:61623
sent reply to 127.0.0.1:61623
```

Sample: Client
---------------

```
telnet 127.0.0.1 6000 
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
WHO
{'127.0.0.1:61389', '127.0.0.1:61390', '127.0.0.1:61394'}
```

