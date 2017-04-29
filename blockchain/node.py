# trade simulation
import hashlib
import select
import socket
import struct
import sys
import time
from threading import Thread, Lock

import chain
import mining
import merkle
import transaction

PRE_FIX_TRANSACTION = '[TRANSACTION]'
PRE_FIX_REQUEST = '[REQUEST_INFO]'
PRE_FIX_BLOCK = '[BLOCK]'
HOST_LIST_SPLIT = '#'
BLOCK_ITEM_SPLIT = '#'
HOST_SPLIT = '-'

class BCNode:
    def __init__(self, host, port_server, node_addr):
        """
        : init socket host(string) | port_server(int)
        """
        self.HOST = host
        self.PORT_SERVER = port_server
        self.SHOW_NODE_ADDR = node_addr

        self.RECV_BUFFER = 4096
        self.MAX_LEN_CONN = 10
        self.FLAG_MINING = True # status of mining
        self.UNMARK_FILE = 'bcinfo/' + str(port_server) + '/transaction'
        self.BC_FILE = 'bcinfo/' + str(port_server) + '/blockchain'
        self.BC_INDEX_FILE = 'bcinfo/' + str(port_server) + '/index.id'     
        self.HOST_FILE = 'bcinfo/' + str(port_server) + '/host'
        self.set_file() # create blockchain and index.id file and transaction

        self.TRANSACTION = set() # transaction information
        self.SOCKET_LIST = []  # connection client socket_list
        self.HOST_LIST = [] # one-step node
        self.get_socket_list(self.HOST_FILE) # get the one-step node
        self.HOST_LIST.append(self.SHOW_NODE_ADDR)

        self.DATA = ''

        self.blockchain = chain.Chain(self.PORT_SERVER)
        self.blockchain.create_first_block('first transaction.')
        
        self.lock = Lock()  # init threading.Lock

    def set_file(self):
        with open(self.BC_FILE, 'w') as tmp: pass
        with open(self.BC_INDEX_FILE, 'w') as tmp: pass
        with open(self.UNMARK_FILE, 'w') as tmp: pass

    def set_data(self, pre_fix, data):
        """
        : set data to string: pre_fix|source_addr|info
        """
        self.DATA = pre_fix + '|' + self.HOST + ' ' + str(self.PORT_SERVER) + '|'
        self.DATA += data if len(data) != 0 else ''

    def get_socket_list(self, fn):
        with open(fn, 'r') as socket_list:
            for line in socket_list.readlines():
                if line[-1] == '\n':
                    line = line[:-1]
                self.HOST_LIST.append(line)

    def start_server(self):
        """
        : start socket server
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket server
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.HOST, self.PORT_SERVER))
        self.server_socket.listen(self.MAX_LEN_CONN)

        self.SOCKET_LIST.append(self.server_socket)
        print('Start trade server.')

    def start_send(self, except_addr):
        """
        : start socket client
        : param: except_addr(string: ip+' '+port)
        """
        for host in self.HOST_LIST:
            if host == except_addr: continue
            host = host.split(' ') # host: [ip(string), port(string)]
            host[1] = int(host[1]) 
            count_flag = 0
            while True:
                try:
                    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client_socket.settimeout(15) 
                    self.client_socket.connect(tuple(host))
                    self.client_socket.send(self.DATA.encode())
                    print("> [1 send to %s]" % host, self.DATA)
                    check_code = self.client_socket.recv(self.RECV_BUFFER)
                    if self.check(check_code, self.DATA, self.client_socket):
                        print('> [2 recv] right info: %s.' % host)
                        self.client_socket.send(b'success')
                        break
                    else:
                        print('> [2 recv] wrong info: %s.' % host)
                        print('> [3 resend] to %s.' % host)
                        count_flag += 1
                        if count_flag <= 3:
                            continue # resend self.DATA
                        else: break
                except Exception as e:
                    print('! node %s' %e)
                finally:
                    self.client_socket.close()

    def check(self, check_code, data, sock):
        """
        : check information which server receives
        """
        origin_data = data
        hash_code = hashlib.sha256(origin_data.encode()).hexdigest().encode()
    
        return True if hash_code == check_code else False

    def send(self, pre_fix, data, except_addr=''):
        """
        : set data information then call self.start_send to send data
        """
        self.set_data(pre_fix, data)
        print('> [0 relay data] %s' % self.DATA)
        self.start_send(except_addr)

    def relay_data(self, data):
        """
        : relay_data
        : param: data(string:pre_fix|source_addr|transaction)
        """
        data_list = data.split('|')
        if data_list[2] not in self.TRANSACTION:
            self.TRANSACTION.add(data_list[2]) # store data in memory(unmark)
            print('write %s into transaction' % data_list[2])
            with open(self.UNMARK_FILE, 'a') as transfer_io:
                transfer_io.write(data_list[2] + '\n') # store data in disk(unmark)
            
            if len(self.SOCKET_LIST) != 0:
                self.send(PRE_FIX_TRANSACTION, data_list[2], data_list[1]) # relay data to one-step node

    def answer_request_info(self, sock):
        """
        : answer_request_info
        """
        with open(self.UNMARK_FILE, 'r') as out:
            data = out.read()
        sock.send(data.encode())

    def valid_block(self, block):
        """
        : valid block merkle_root
        """
        # end the mining 
        # to do
        DATA_SPLIT = '|'
        BLOCK_ITEM_SPLIT = '#'
        TRANSACTION_SPLIT = '$'

        info_list = block.split(DATA_SPLIT)
        block_str = info_list[2]
        block_list = block_str.split(BLOCK_ITEM_SPLIT)
        # len_data = block_list[chain.LENGTH]
        b_data_list = block_list[chain.DATA].split(TRANSACTION_SPLIT)
        len_transaction = len(b_data_list)
        
        if len(self.TRANSACTION) != len_transaction:
            pass
        else:
            last_block = self.blockchain.last_block()
            data = last_block[-1]

            if block_list[chain.PREV_HASH] != last_block[chain.MERKLE_ROOT]:
                print('different hash')
                return
            for item in b_data_list:
                if item not in self.TRANSACTION:
                    print('different transaction')
                    return
                else:
                    self.TRANSACTION.remove(item)

            self.blockchain.add_block(b_data_list)
            with open(self.UNMARK_FILE, 'w') as tmp:
                for item in self.TRANSACTION:
                    tmp.write(item+'\n')
            
            self.send(PRE_FIX_BLOCK, block_str)

        

            # start the mining 
            # to do

    def receive(self):
        """
        : receive rules in server socket
        """
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
                            # print('> [recv](%s@%s) receives info.' % addr)
                            check_data = sock.recv(self.RECV_BUFFER).decode() # check status
                            if check_data == 'success':
                                if data.startswith(PRE_FIX_TRANSACTION):
                                    self.relay_data(data)
                                elif data.startswith(PRE_FIX_REQUEST):
                                    self.answer_request_info(sock)
                                elif data.startswith(PRE_FIX_BLOCK):
                                    self.valid_block(data)
                        else:
                            print('> [recv](%s@ %s) is offline.' % addr)
                        self.SOCKET_LIST.remove(sock)
                    except Exception as e:
                        print('! node receive: %s.' % e)
                        self.SOCKET_LIST.remove(sock)
        self.server_socket.close()


def argv_format(hosts_str):
    hosts_list = hosts_str[:-1].split(HOST_LIST_SPLIT)
    for i in range(len(hosts_list)):
        tmp_list = hosts_list[i].split(HOST_SPLIT)
        hosts_list[i] = ' '.join(tmp_list)
    return hosts_list


def run():
    if len(sys.argv) >= 2:
        print("node.py: start_server sys.argv: %s" % str(sys.argv))
        host = sys.argv[1]
        show_node_addr = sys.argv[4] + ' '+ '9999'
        port = int(sys.argv[2])
        hosts_list = argv_format(sys.argv[3])
        print(hosts_list)
        bcnode = BCNode(host, port, show_node_addr)
        bcnode.start_server()
        Thread(target=bcnode.receive).start()
        # time.sleep(5)
        Thread(target=transaction.send, args=(bcnode, hosts_list)).start()
        time.sleep(2)
        Thread(target=mining.run, args=(bcnode,)).start()  # note that: (,)
    else:
        print('wrong parm.')


def test(ip, port, host_list):
    hosts_list = argv_format(host_list)
    bcnode = BCNode(ip, port)
    bcnode.start_server()
    Thread(target=bcnode.receive).start()
    time.sleep(10)
    Thread(target=transaction.send, args=(bcnode, hosts_list)).start()
    time.sleep(10)
    Thread(target=mining.run, args=(bcnode,)).start()


if __name__ == '__main__':
    run() # run
    # test('', 9000, '127.0.0.1-9000#127.0.0.1-9002#127.0.0.1-9003#') # test