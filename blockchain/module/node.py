# trade simulation
import sys
import socket
import select
import hashlib
import transaction

PRE_FIX_TRANSACTION = '[TRANSACTION]'
PRE_FIX_REQUEST = '[REQUEST_INFO]'
PRE_FIX_BLOCK = '[BLOCK]'

class BCNode:
    def __init__(self, host, port_server):
        '''
        : init socket host(string) | port_server(int)
        '''
        self.HOST = host
        self.PORT_SERVER = port_server

        self.RECV_BUFFER = 4096
        self.MAX_LEN_CONN = 10
        self.FLAG_MINING = True # status of mining
        self.UNMARK_FILE = 'unmark'

        self.TRANSACTION = set() # transaction information
        self.SOCKET_LIST = []  # connection client socket_list
        self.HOST_LIST = [] # one-step node
        self.get_socket_list('host/'+str(self.PORT_SERVER)) # get the one-step node

        self.DATA = ''

    def set_data(self, pre_fix, data):
        '''
        : set data to string: pre_fix|source_addr|info
        '''
        self.DATA = pre_fix + '|' + self.HOST + ' ' + self.PORT_SERVER + '|'
        self.DATA += data if len(data) != 0 else ''

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
        : param: except_addr(string: ip+' '+port)
        '''
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)

        for host in self.HOST_LIST:
            if len(except_addr) == 0 or host == except_addr:
                continue # except source_host
                
            host = host.split(' ') # host: [ip(string), port(string)]
            host[1] = int(host[1]) 

            # if host[1] == self.PORT_SERVER and host[0] == self.HOST: 
            #     continue # except itself
            
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

    def send(self, pre_fix, data, except_addr = ''):
        '''
        : set data information then call self.start_send to send data
        '''
        self.set_data(pre_fix, data)
        print('> [1 sending] %s' % self.DATA)
        self.start_send(except_addr)

    def relay_data(self, transfer_io, data):
        '''
        : relay_data
        : param: data(string:pre_fix|source_addr|transaction)
        '''
        data_list = data.split('|')
        if data_list not in self.TRANSACTION:
            self.TRANSACTION.add(data_list[2]) # store data in memory(unmark)
            transfer_io.write(data_list[2]) # store data in disk(unmark)
            transfer_io.flush()

            if len(self.SOCKET_LIST) != 0:
                self.send(PRE_FIX_TRANSACTION, data, data_list[1]) # relay data to one-step node

    def answer_request_info(self, sock):
        '''
        : answer_request_info
        '''
        with open(self.UNMARK_FILE, 'r') as out:
            data = out.read()
        sock.send(data.encode())

    def valid_block(self, block):
        '''
        : answer_request_info
        '''
        pass

    def receive(self):
        '''
        : receive rules in server socket
        '''
        transfer_io = open(self.UNMARK_FILE, 'a')

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
                                if data.startswith(PRE_FIX_TRANSACTION):
                                    self.relay_data(transfer_io, data)
                                elif data.startswith(PRE_FIX_REQUEST):
                                    self.answer_request_info(sock)
                                elif data.startswith(PRE_FIX_BLOCK):
                                    self.valid_block(data)
                        else:
                            print('> [recv](%s@ %s) is offline.' % addr)
                        self.SOCKET_LIST.remove(sock)
                    except Exception as e:
                        print('! 132: %s.' % e)
                        self.SOCKET_LIST.remove(sock)
        self.server_socket.close()


def start_server():
    if len(sys.argv) >= 2:
        print("138: start_server sys.argv: %s" % str(sys.argv))
        host = sys.argv[1]
        port = int(sys.argv[2])
        hosts_list = sys.argv[3].split('#')
        bcnode = BCNode(host, port)
        bcnode.start_server()
        bcnode.receive()
        transaction.send(bcnode, hosts_list)
    else:
        print('wrong parm.')

# # test
# if __name__ == '__main__':
#     start_server()
