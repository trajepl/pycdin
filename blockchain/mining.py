import time
import random
import struct
import socket
from node import PRE_FIX_BLOCK
from block import RAND_NUM, RAND_RANGE, PACK_FORMAT

BC_FILE = 'blockchain'


def read_unmark_clear(bcnode):
    """
    : read file unmark and truncate it
    """
    transaction_list = []
    tmp_transactions = bcnode.TRANSACTION
    len_transaction = len(tmp_transactions)

    print('mining %s' % bcnode.TRANSACTION)
    for item in tmp_transactions:
        transaction_list.append(item)
    # lock.acquire()
    bcnode.TRANSACTION = set(list(bcnode.TRANSACTION)[len_transaction:])

    with open(bcnode.UNMARK_FILE, 'w') as tmp: 
        for item in bcnode.TRANSACTION:
            tmp.write(item + '\n')
    # lock.release()

    return transaction_list


def mining(bcnode):
    transaction_list = read_unmark_clear(bcnode)
    if len(transaction_list) == 0: return
    new_block = bcnode.blockchain.add_block(transaction_list)

    len_data = new_block.length
    block_bytes = new_block.bytesstr()
    block_tuple = struct.unpack(PACK_FORMAT+str(len_data)+'s', block_bytes)
    print(block_tuple)
    block_str = ''
    for item in block_tuple:
        if isinstance(item, bytes):
            item = item.decode()
        block_str += str(item) + '#'
    send_block(bcnode, block_str[:-1])


def pow_simulator(rand_number):
    while random.randint(-RAND_RANGE, RAND_RANGE) != rand_number:
            continue  # pow simulator


def send_block(bcnode, block_str):
    # set data format
    data = PRE_FIX_BLOCK + '|' + bcnode.HOST + ' ' + str(bcnode.PORT_SERVER) + '|'
    data += block_str if len(block_str) != 0 else ''

    # boradcast
    for host in bcnode.HOST_LIST:
        host = host.split(' ')
        host[1] = int(host[1])    
        while True:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(15)
                client_socket.connect(tuple(host))
                client_socket.send(data.encode())
                print("> [1 send to %s]" % host, data)

                check_code = client_socket.recv(bcnode.RECV_BUFFER)
                if bcnode.check(check_code, data, client_socket):
                    print('> [3 recv] right info: %s.' % host)
                    client_socket.send(b'success')
                    break
                else:
                    print('> [3 recv] wrong info: %s.' % host)
                    print('> [4 resend] to %s.' % host)
                    continue
            except Exception as e:
                print('! mining %s' %e)
            finally:
                client_socket.close()
        

def run(bcnode):
    while True:
        block_prefix, index_item = bcnode.blockchain.last_block_prefix()
        rand_number = int(block_prefix[RAND_NUM])  # get rand_num of last block
        print('begin  mining: %d' %rand_number)
        pow_simulator(rand_number)
        mining(bcnode)
        time.sleep(10) # begin new mining after 10s

