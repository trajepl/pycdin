# trade simulation
import sys
import socket
import select
import hashlib


class Trade:
    def __init__(self, host, port_server):
        '''
        : init socket host(string) | port_server(int)
        '''
        self.HOST = host
        self.PORT_SERVER = port_server

        self.RECV_BUFFER = 4096
        self.MAX_LEN_CONN = 10

        self.SOCKET_LIST = []  # connection client socket_list
        self.TRANSACTION = set() # transaction information
        self.HOST_LIST = [] # one-step node
        self.get_socket_list('host/'+str(self.PORT_SERVER)) # get the one-step node

        self.DATA = "" 

    def set_data(self, data):
        if len(data) != 0:
            self.DATA = data

    def get_socket_list(self, fn):
        with open(fn, 'r') as socket_list:
            for line in socket_list.readlines():
                self.HOST_LIST.append(line)

    def start_server(self):
        '''
        : start socket server
        '''
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket server
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.HOST, self.PORT_SERVER))
        self.server_socket.listen(self.MAX_LEN_CONN)

        self.SOCKET_LIST.append(self.server_socket)
        print('Start trade server.')

    def start_send(self):
        '''
        : start socket client
        '''
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)

        for host in self.HOST_LIST:
            host = host.split(' ') # host: [ip(string), port(string)]
            host[1] = int(host[1]) 

            if host[1] == self.PORT_SERVER and host[0] == self.HOST: 
                continue # except itself
            
            while True:
                print("$ [2 send to]: %s" % host)
                try:
                    self.client_socket.connect(tuple(host))
                    self.client_socket.send(self.DATA.encode())
                except Exception as e:
                    print('! 59: %s %s' % (e, host))

                try:
                    check_code = self.client_socket.recv(self.RECV_BUFFER)
                    if self.check(check_code, self.client_socket):
                        print('> [3 recv] right info: %s.' % host)
                        self.client_socket.send(b'success')
                    else:
                        print('> [3 recv] wrong info: %s.' % host)
                        print('> [4 resend] to %s.' % host)
                        continue # resend self.DATA
                except Exception as e:
                    print('! 67: %s %s' % (e, host))
                finally:
                    self.client_socket.close()
                    break

    def check(self, check_code, sock):
        '''
        : check information which server receives
        '''
        origin_data = ''
        for item in self.DATA:
            origin_data += item
        hash_code = hashlib.sha256(origin_data.encode()).hexdigest().encode()
    
        return True if hash_code == check_code else False

    def send(self, data):
        '''
        : set data information then call self.start_send to send data
        '''
        self.set_data(data)
        print('> [1 sending] %s' % self.DATA)
        self.start_send()

    def receive(self):
        '''
        : receive rules in server socket
        '''
        while True:
            ready_to_read, read_to_write, in_error = select.select(self.SOCKET_LIST, [], [], 0)
            for sock in ready_to_read:
                if sock == self.server_socket: 
                    sockfd, addr = self.server_socket.accept()
                    self.SOCKET_LIST.append(sockfd) # a new connection request received
                else:
                    try:
                        data_bytes = sock.recv(self.RECV_BUFFER) # receive data
                        data = data_bytes.decode()
                        check_code = hashlib.sha256(data_bytes).hexdigest().encode()

                        if len(data) != 0:
                            sock.send(check_code)
                            print('> [recv](%s@%s) receives info.' % addr)
                            check_data = sock.recv(self.RECV_BUFFER).decode() # check status
                            if check_code == 'success':
                                self.TRANSACTION.add(data)
                                if len(self.SOCKET_LIST) != 0:
                                    self.DATA = data
                                    self.start_send() # transmit data to one-step node
                        else:
                            print('> [recv](%s@ %s) is offline.' % addr)
                        self.SOCKET_LIST.remove(sock)
                    except Exception as e:
                        print('! 132: %s.' % e)
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

# # test
# if __name__ == '__main__':
#     start_server('127.0.0.1', 8000)
