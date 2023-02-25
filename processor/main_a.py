
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import socket
import json

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 60007

KEY = "aaa"

running = True

def nop(key:str, **kwargs):
    pass

def init(key:str, **kwargs):
    print(key)
    print("init")
    conn.send("c:bbb:objprint:{'data':'call from aaa'};".encode("ascii"))

def objprint(key:str, data:str, **kwargs):
    print(data)

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((SERVER_HOST, SERVER_PORT))
conn.send(("c:%s:init:{};" % KEY).encode("ascii"))
print("c:%s:init:{};" % KEY)
call = ""
conn.send(("p:%s;" % KEY).encode("ascii"))
print("p:%s;" % KEY)
while running:
    b = ""
    try:
        b = conn.recv(1).decode("ascii")
        if b == "":
            continue
        elif b != ";":
            call += b
            continue
    except TimeoutError:
        continue
    except:
        conn.close()
        break
    if call:
        print(call)
        call = call.split(":", 2)
        print(call)
        key = call[0]
        method = globals().get(call[1], nop)
        kwargs = json.loads(call[2])
        method(key=key, **kwargs)
    call = ""
    conn.send(("p:%s;" % KEY).encode("ascii"))
    print("p:%s;" % KEY)
