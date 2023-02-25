
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import socket
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 60007

PROCESSOR_COUNT = 8

queue = []
queue_lock = threading.Lock()

running = True
processors = [None for _ in range(PROCESSOR_COUNT)]
keyed = ["" for _ in range(PROCESSOR_COUNT)]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_HOST, SERVER_PORT))
server.settimeout(3)
server.listen()

def run_thread(index : int):
    while running:
        try:
            conn, addr = server.accept()
            mesg = ""
            while running:
                try:
                    b = conn.recv(1).decode("ascii")
                    if b == "":
                        conn.close()
                        break
                    elif b != ";":
                        mesg += b
                        continue
                except TimeoutError:
                    continue
                except:
                    conn.close()
                    break

                print(mesg)
                if mesg.startswith("c:"):
                    queue.append(mesg[2:])
                    print(mesg[2:])
                    print(queue)
                elif mesg.startswith("p:"):
                    key = mesg[2:]
                    print(key)
                    call = ""
                    with queue_lock:
                        keyed[index] = ""
                        for i in range(len(queue)):
                            c = queue[i].split(":", 1)
                            if c[0].startswith(key) and not c[0] in keyed:
                                call = queue.pop(i)
                                keyed[index] = c[0]
                                print(call)
                                break
                    conn.send((call + ";").encode("ascii"))
                mesg = ""
            
        except TimeoutError:
            continue
        except:
            pass

for index in range(PROCESSOR_COUNT):
    processors[index] = threading.Thread(target=run_thread, kwargs={"index":index})
    processors[index].start()
