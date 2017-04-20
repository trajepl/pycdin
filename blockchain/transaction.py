# broadcast msg
import sys
import time
import random
import socket
from threading import Timer

import node

SEND_INTERVAL = 10
TIMER_SEND  = None
   
def random_send(bcnode, hosts_list):

    """
    : set fixed time (interval 10s) to randomly selectting a source host sending data
    """
    is_continue = random.choice([True, False])
    if is_continue :
        data = random_data(hosts_list)
        bcnode.TRANSACTION.add(data)
        send_transaction(bcnode, data)
    else:
        pass

    global TIMER_SEND
    TIMER_SEND = Timer(SEND_INTERVAL, random_send, args=(bcnode, hosts_list))
    TIMER_SEND.start()


def random_data(hosts_list):
    """
    : transaction data
    """
    trade_double = random.sample(hosts_list, 2)
    coin_num = random.randint(1, 100)
    return str(trade_double[0]) + ' trasfer ' + str(coin_num) + \
           ' bitcoins to ' + str(trade_double[1]) + '.'

def send_transaction(bcnode, transaction_str):
    # set data format
    data = node.PRE_FIX_TRANSACTION + '|' + bcnode.HOST + ' ' + str(bcnode.PORT_SERVER) + '|'
    data += transaction_str if len(transaction_str) != 0 else ''

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
                print('! transaction %s' %e)
            finally:
                client_socket.close()
            

def send(bcnode, hosts_list):
    """
    : start timer
    """
    global TIMER_SEND
    TIMER_SEND = Timer(SEND_INTERVAL, random_send, args=(bcnode, hosts_list))
    TIMER_SEND.start()
