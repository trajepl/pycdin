# trade simulation
import sys
import socket
import select
import hashlib

from threading import Thread


class Trade:
    def __init__(self, host, port_server):
        self.HOST = host
        self.SOCKET_LIST = []
        self.HOST_LIST = []
        self.RECV_BUFFER = 4096
        # self.PORT_SERVER = 8081
        self.PORT_SERVER = port_server
        self.MAX_LEN_CONN = 10
        self.DATA = []

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print('24: Trade [%s %s]' %(self.HOST, self.PORT_SERVER))
        self.get_socket_list('host/'+str(self.PORT_SERVER))

    def set_data(self, data):
        if len(data) != 0:
            self.DATA.append(data+' | ')

    def set_host(self, host, port_server):
        self.HOST = host
        self.PORT_SERVER = port_server

    def set_max_len_conn(self, num):
        self.MAX_LEN_CONN = num

    def start_server(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.HOST, self.PORT_SERVER))
        self.server_socket.listen(self.MAX_LEN_CONN)

        self.SOCKET_LIST.append(self.server_socket)

        print('Start tcp server.')

    def start_send(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)

        for host in self.HOST_LIST:
            host = host.split(' ')

            # cluster debug
            host[1] = int(host[1])
            # host[0] == self.HOST

            if host[1] == self.PORT_SERVER:
                continue

            print("$ [send to]: %s" % host)
            try:
                self.client_socket.connect(tuple(host))
                data_item = ''
                for item in self.DATA:
                    data_item += item
                self.client_socket.send(data_item.encode())
            except Exception as e:
                print('! line 59: %s %s' % (e, host))
            try:
                check_code = self.client_socket.recv(self.RECV_BUFFER)
                if self.check(check_code, self.client_socket):
                    print('> [recv] right info: %s.' % host)
                else:
                    print('> [recv] wrong info: %s.' % host)
                    print('> [resend] to %s.' % host)
            except Exception as e:
                print('! line 67: %s %s' % (e, host))

    def get_socket_list(self, fn):
        with open(fn, 'r') as socket_list:
            for line in socket_list.readlines():
                self.HOST_LIST.append(line)

    def check(self, check_code, sock):
        origin_data = ''
        for item in self.DATA:
            origin_data += item

        hash_code = hashlib.sha256(origin_data.encode()).hexdigest().encode()

        if hash_code == check_code:
            sock.send(b'True')
            return True
        else:
            sock.send(b'False')
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
                        data_bytes = sock.recv(self.RECV_BUFFER)
                        data = data_bytes.decode()
                        check_code = hashlib.sha256(data_bytes).hexdigest().encode()

                        if len(data) != 0:
                            sock.send(check_code)
                            print('> [recv](%s@%s) receives info.' % addr)
                            print('> ' + data + ':' + check_code.decode())
                        else:
                            print('> [recv](%s@ %s) is offline.' % addr)
                        self.SOCKET_LIST.remove(sock)
                    except Exception as e:
                        print(e)
                        self.SOCKET_LIST.remove(sock)
        self.server_socket.close()

    def send(self):
        while True:
            self.DATA = []
            data = ''
            while data != '#':
                self.set_data(data)
                data = input("> [send](exit with '#'):")
            print('> [sending] %s' % self.DATA)
            self.start_send()


def start_server(host, port):
    trade = Trade(host, port)
    trade.start_server()
    server = Thread(target=trade.receive)
    server.start()
    client = Thread(target=trade.send)
    client.start()


# def mul_thread(fn):
#     with open(fn, 'r') as host_in:
#         for line in host_in.readlines():
#             Thread(target=main).start()


if __name__ == '__main__':
    start_server('127.0.0.1', 8000)
