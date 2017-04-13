# trade simulation
import hashlib
import select
import socket
import struct
import sys
import time
import chain

PRE_FIX_TRANSACTION = '[TRANSACTION]'
PRE_FIX_BLOCK = '[BLOCK]'
HOST_LIST_SPLIT = '#'
HOST_SPLIT = '-'

class BCNode:
    def __init__(self, host, port_server):
        """
        : init socket host(string) | port_server(int)
        """
        self.HOST = host
        self.PORT_SERVER = port_server

        self.RECV_BUFFER = 4096
        self.MAX_LEN_CONN = 10

        self.UNMARK_FILE = 'bcinfo/' + str(port_server) + '/transaction'
        self.BC_FILE = 'bcinfo/' + str(port_server) + '/blockchain'
        self.BC_INDEX_FILE = 'bcinfo/' + str(port_server) + '/index.id'     
        self.HOST_FILE = 'bcinfo/' + str(port_server) + '/host'
        self.set_file() # create blockchain and index.id file and transaction

        self.TRANSACTION = set() # transaction information
        self.SOCKET_LIST = []  # connection client socket_list

        self.get_socket_list(self.HOST_FILE) # get the one-step node

        self.DATA = ''

        self.blockchain = chain.Chain(self.PORT_SERVER)
        self.blockchain.create_first_block('first transaction.')

    def set_file(self):
        mkdir('bcinfo/'+str(self.PORT_SERVER))
        with open(self.BC_FILE, 'w') as tmp: pass
        with open(self.BC_INDEX_FILE, 'w') as tmp: pass
        with open(self.UNMARK_FILE, 'w') as tmp: pass

    def set_data(self, pre_fix, data):
        """
        : set data to string: pre_fix|source_addr|info
        """
        self.DATA = pre_fix + '|' + self.HOST + ' ' + str(self.PORT_SERVER) + '|'
        self.DATA += data if len(data) != 0 else ''

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

    def recv_block(self, block):
        """
        : valid block merkle_root
        """
        block_prefix = struct.unpack(chain.PACK_FORMAT, block[:chain.LEN_PRE_DATA].encode())
        len_data = block_prefix[chain.LENGTH]
        b_data = struct.unpack(str(len_data)+'s', block[chain.LEN_PRE_DATA:].encode())
        b_data_list = b_data.split('|')
        len_transaction = len(b_data_list)

        if len(self.TRANSACTION) != len_transaction:
            pass
        else:
            '''
            : when the merkle_root same pass.(order same)
            '''
            last_block = self.blockchain.last_block()
            data = last_block[-1]
            for item in self.TRANSACTION:
                if item not in data:
                    return
            self.blockchain.write_exist_block(block.encode(), 'ab', len_data)

            self.TRANSACTION = set(list(self.TRANSACTION)[len_transaction:])
            with open(self.UNMARK_FILE, 'w') as tmp:
                for item in self.TRANSACTION:
                    tmp.write(item+'\n')

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
                            print('> [recv](%s@%s) receives info.' % addr)
                            check_data = sock.recv(self.RECV_BUFFER).decode() # check status
                            if check_data == 'success':
                                if data.startswith(PRE_FIX_TRANSACTION):
                                    self.relay_data(data)
                                elif data.startswith(PRE_FIX_BLOCK):
                                    self.recv_block(data)
                        else:
                            print('> [recv](%s@ %s) is offline.' % addr)
                        self.SOCKET_LIST.remove(sock)
                    except Exception as e:
                        print('! 132: %s.' % e)
                        self.SOCKET_LIST.remove(sock)
        self.server_socket.close()


def run():
    show_node = ShowNode('', 9999)
    show_node.start_server()
    show_node.receive()


if __name__ == '__main__':
    run()
    