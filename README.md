Socketz
============
![socket](https://github.com/r3lik/socketz/blob/master/media/socket.png)

A simple TCP server written in Python. It uses [HAProxy](https://github.com/haproxy/haproxy) for L4 load-balancing/HA and clustered [etcd](https://github.com/etcd-io/etcd) for state replication.

![screencap](https://github.com/r3lik/socketz/blob/master/media/socket_v2.gif)

Requirements
--------------
* Python 3.0+
* Docker
* Docker Compose

Usage
------------
* `docker-compose up -d` to provision network, download images and launch containers
* `docker exec -it client01 /usr/bin/telnet frontend.socketz.gg 4141`... `client04` to mimic outside client connections
* `docker kill server01` to demonstrate that new requests roundrobin to healthy servers only via `HAProxy`
* `docker kill etcd01` to demonstrate that DNS roundrobin will use working connections
* `docker exec etcd01 /bin/sh -c "export ETCDCTL_API=3 && /usr/local/bin/etcdctl member list"` to list nodes in cluster


HAProxy stats
-------------
* `haproxy01` `http://localhost:9000/stats`
* `haproxy02` `http://localhost:9001/stats`
* `haproxy03` `http://localhost:9002/stats`

default credentials: admin:hodl

Commands
-------------
* `WHO` shows clients connected to all available servers and locally connected clients (via HAProxy)
* `WHERE` outputs the id of the server (unique identifier)
* `WHY` outputs the string "42" ;]
* `QUIT` terminates session :wave:

Flags (to pass to Docker)
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
Trying 172.60.0.2...
Connected to frontend.socketz.gg.
Escape character is '^]'.
WHO
IP:PORT of clients connected to this server: {'172.60.0.3:45274', '172.60.0.4:33078', '172.60.0.2:44592'}
clients connected to this server: 3
clients connected to all servers: 5
WHERE
08483048-fdb7-4648-9f00-c505e1207df4
```

State replication and fault tolerance
-------------------------------------
This is accomplished by running a three member cluster of etcd with HAProxy load balancing client requests. etcd is the source of truth for all three of the backend Python servers. Consistency is enforced by Raft, the consensus algorithm used by etcd. For etcd HA is achieved through a combination of [clustering](https://github.com/etcd-io/etcd/blob/master/Documentation/faq.md#what-is-failure-tolerance) (failure tolerance 1 with a 3 node cluster) and pointing to a DNS roundrobin'ed FQDN, so that requests hit the next available host ([RFC 1794](http://www.faqs.org/rfcs/rfc1794.html)). It's worth noting that Docker DNS handles this differently as it pulls the A record out. For the TCP servers, HA is achieved by the use of HAProxy roundrobin proxy with 2s check intervals, as well as DNS roundrobin.

```
root@client02:/# dig frontend.socketz.gg +short
172.60.0.3
172.60.0.2
172.60.0.4

root@client02:/# dig etcd-cluster.socketz.gg +short
172.60.0.22
172.60.0.21
172.60.0.23
```

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
This shows that a key:value pair put on `etcd01` is made available to `etcd02` and `etcd03` via the Raft consensus algorithm. If one dies, it will "re-sync" when it rejoins the cluster.
