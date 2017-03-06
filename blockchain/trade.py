# trade simulation
import sys
import socket
import select
import hashlib

class Trade:
    def __init__(self):
        self.HOST = ''
        self.SOCKET_LIST = []
        self.HOST_LIST = []
        self.RECV_BUFFER = 4096
        self.PORT_SERVER = 9091
        self.PORT_CLIENT = 9090
        self.MAX_LEN_CONN = 10
        self.DATA = []

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.get_socket_list('hostlist')

    def set_data(self, data):
        self.DATA.append(data)

    def set_host(self, host, port_server, port_client):
        self.HOST = host
        self.PORT_SERVER = port_server
        self.PORT_CLIENT = port_client

    def set_max_len_conn(self, num):
        self.MAX_LEN_CONN = num

    def start_server(self):
        self.server_socket.bind((self.HOST, self.PORT_SERVER))
        self.server_socket.listen(self.MAX_LEN_CONN)

        self.SOCKET_LIST.append(self.server_socket)

        print('Start tcp server.')

    def start_send(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)

        for host in self.HOST_LIST:
            host = host.split(' ')
            host[1] = int(host[1])

            try:
                self.client_socket.connect(tuple(host))
                for item in self.DATA:
                    self.client_socket.send(str(item).encode())
            except Exception as e:
                print(e)
                sys.exit()

    def get_socket_list(self, fn):
        with open(fn, 'r') as socket_list:
            for line in socket_list.readlines():
                self.HOST_LIST.append(line)

    def check(self, check_code):
        origin_data = ''
        for item in self.DATA:
            origin_data += item

        hash_code = hashlib.sha256(origin_data).hexdigest().encode()

        if hash_code == check_code:
            self.server_socket.send(b'True')
            return True
        else:
            self.server_socket.send(b'False')
            return False

    def receive(self, ):
        while True:
            ready_to_read, read_to_write, in_error = select.select(self.SOCKET_LIST, [], [], 0)
            for sock in ready_to_read:
                # a new connection request received
                if sock == self.server_socket:
                    sockfd, addr = self.server_socket.accept()
                    self.SOCKET_LIST.append(sockfd)
                else:
                    try:
                        data = sock.recv(self.RECV_BUFFER)
                        data = data.decode()
                        check_ret = self.check(data)

                        if len(data) != 0 and check_ret:
                            print('> [%s@ %s] receives right info.' % addr)
                        elif not check_ret:
                            print('> [%s@ %s] receives wrong info. Resending...' % addr)
                            self.server_socket.send(self.DATA[0].encode())
                        else:
                            print('> [%s@ %s] is offline.' % addr)
                            self.SOCKET_LIST.remove(sock)
                    except:
                        print('> [%s@ %s] is offline.' % addr)
                        self.SOCKET_LIST.remove(sock)
        self.server_socket.close()

if __name__ == '__main__':
    trade = Trade()
    trade.start_server()
    trade.set_host('127.0.0.1', 9090, 8090)
    data = input('> ')

    trade.set_data(data)
    trade.start_send()
