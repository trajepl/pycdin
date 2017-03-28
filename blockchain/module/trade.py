# trade simulation
import sys
import socket
import select
import hashlib


class Trade:
    def __init__(self, host, port_server):
        self.HOST = host
        self.SOCKET_LIST = []
        self.HOST_LIST = []
        self.RECV_BUFFER = 4096
        # self.PORT_SERVER = 8081
        self.PORT_SERVER = port_server
        self.MAX_LEN_CONN = 10
        self.TRANSACTION = set()
        self.DATA = ""

        # socket server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # get the one-step node
        self.get_socket_list('host/'+str(self.PORT_SERVER))

    def set_data(self, data):
        if len(data) != 0:
            self.DATA = data

    def set_host(self, host, port_server):
        self.HOST = host
        self.PORT_SERVER = int(port_server)

    def set_max_len_conn(self, num):
        self.MAX_LEN_CONN = num

    def get_socket_list(self, fn):
        with open(fn, 'r') as socket_list:
            for line in socket_list.readlines():
                self.HOST_LIST.append(line)

    def start_server(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.HOST, self.PORT_SERVER))
        self.server_socket.listen(self.MAX_LEN_CONN)

        self.SOCKET_LIST.append(self.server_socket)
        print('Start trade server.')

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
                self.client_socket.send(self.DATA.encode())
            except Exception as e:
                print('! line 59: %s %s' % (e, host))
            try:
                check_code = self.client_socket.recv(self.RECV_BUFFER)
                if self.check(check_code, self.client_socket):
                    print('> [recv] right info: %s.' % host)
                    self.client_socket.send(b'success')
                else:
                    print('> [recv] wrong info: %s.' % host)
                    print('> [resend] to %s.' % host)
            except Exception as e:
                print('! line 67: %s %s' % (e, host))
            finally:
                # close the client
                self.client_socket.close()


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

    def send(self, data):
        self.set_data(data)
        print('> [sending] %s' % self.DATA)
        self.start_send()

    def receive(self):
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
                            check_data = sock.recv(self.RECV_BUFFER).decode()
                            if check_code == 'success':
                                self.TRANSACTION.add(data)
                                if len(self.SOCKET_LIST) != 0:
                                    self.DATA = data
                                    self.start_send()
                        else:
                            print('> [recv](%s@ %s) is offline.' % addr)
                        self.SOCKET_LIST.remove(sock)
                    except Exception as e:
                        print(e)
                        self.SOCKET_LIST.remove(sock)
        self.server_socket.close()


def start_server(host, port):
    if len(sys.argv) >= 2:
        print("138: start_server sys.argv: %s" % str(sys.argv))
        host = sys.argv[1]
        port = int(sys.argv[2])
        trade = Trade(host, port)
        trade.start_server()
        trade.receive()
    else:
        print('wrong parm.')


# if __name__ == '__main__':
#     start_server('127.0.0.1', 8000)
