# broadcast msg
import sys
import time
import random
from threading import Timer

import node

SEND_INTERVAL = 10
# TIMER_SEND  = None
   
def random_send(bcnode, data, hosts_list):
    '''
    : set fixed time (interval 10s) to randomly selectting a source host sending data
    '''
    is_continue = random.choice([True, False])
    if is_continue :
        src_hosts = random.choice(hosts_list)
        src_host = src_hosts[0]
        src_port = src_hosts[1]
        except_addr = src_host + ' ' + str(src_port)
        print('TRANSACTION 17 src_hosts: ' + str(src_hosts))
        bcnode.send(node.PRE_FIX_TRANSACTION, data, except_addr)
    else:
        pass
    # global TIMER_SEND

    TIMER_SEND = Timer(SEND_INTERVAL, random_send, args=(bcnode, data, hosts_list))
    TIMER_SEND.start()

def random_data(hosts_list):
    '''
    : trasfaction data
    '''
    trade_double = random.sample(hosts_list, 2)
    coin_num = random.randint(1, 100)
    return str(trade_double[0]) + ' trasfer ' + str(coin_num) + \
        ' bitcoins to '+ str(trade_double[1]) + '.'

def send(bcnode, hosts_list):
    '''
    : start timer
    '''
    data = random_data(hosts_list)
    
    # global TIMER_SEND
    TIMER_SEND = Timer(SEND_INTERVAL, random_send, args=(bcnode, data, hosts_list))
    TIMER_SEND.start()