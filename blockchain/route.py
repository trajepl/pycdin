# route control
import os
import sys
import socket
import hashlib
import json

from trade import start_server

PRE_FIX_ROUTE = '[ROUTE]'
PRE_FIX_PROCESS = '[PROCESS]'
BC_BASE_PATH = 'bcinfo/'

def mkdir(path):
    is_exists=os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
        return True
    else:
        return False

class RouteControl:
    def __init__(self, host, port_server):
        self.HOST = host
        self.PORT = port_server
        self.RECV_BUFFER = 1024
        self.MAX_LEN_CONN = 10
        self.SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.BC_HOST_FILE = BC_BASE_PATH + str(port_server) + '/host'
        self.set_bc_host_dir()
    
    def set_bc_host_dir(self):
        tmp_dir = BC_BASE_PATH + str(port_server)
        mkdir(tmp_dir)
        
    def start_server(self):
        self.SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.SERVER_SOCKET.bind((self.HOST, self.PORT))
        self.SERVER_SOCKET.listen(self.MAX_LEN_CONN)

        print('Start tcp server.')
    
    def receive(self):
        len_route = len(PRE_FIX_ROUTE)
        len_process = len(PRE_FIX_PROCESS)
        while True:
            client_sock, add = self.SERVER_SOCKET.accept()
            
            while True:
                data = client_sock.recv(self.RECV_BUFFER)
                data = data.decode()
                if data[0:len_route] == PRE_FIX_ROUTE:
                    data = data[len_route:]
                    route_dir = json.loads(data)
                    print("39: route route_dir: %s" %route_dir)
                    for key in route_dir:
                        origin_route_info = route_dir[key]
                        route_info = origin_route_info.split('|')[:-1]
                        with open(self.BC_HOST_FILE, 'w') as route_out:
                            for info in route_info:
                                route_out.write(info+'\n')

                    client_sock.send(b'success')
                    client_sock.close()
                    break
                elif data[0:len_process] == PRE_FIX_PROCESS:
                    data = data[len_process:].split('|')
                    
                    addr_host = data[0]
                    addr_port = data[1]
                    host_list_str = data[2]
                    os.system('python node.py %s %s &' %(addr_host, addr_port, host_list_str))
                    # start_server(addr_host, int(addr_port))
                    client_sock.send(b'success')
                    client_sock.close()
                    break
                else:
                    client_sock.send(b"Message format badly.")
                    client_sock.close()
    
if __name__ == "__main__":
    route = RouteControl('127.0.0.1', 8100)
    route.start_server()
    route.receive()
