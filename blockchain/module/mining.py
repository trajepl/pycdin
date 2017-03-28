# broadcast msg
import sys
sys.path.append('../')
import trade

import random
import time
from threading import Timer

MINE_INTERVAL = 10 * 60

def broadcast_msg_timer(data, host, port):
    '''
    : (host, port) broadcasts trasfer data to its first-step node.
    '''
    send_process = trade.Trade(host, int(port))
    send_process.send(data)
   
def mine(process, timestamp):
    '''
    : set fixed time (intercal 10s) to randomly selectting a source host sending data
    '''
    is_continue = random.choice([True, False])
    if is_continue :
        src_hosts = random.choice(hosts_list)
        src_host = src_hosts[0]
        src_port = src_hosts[1]
        print('    17: ' + str(src_hosts))
        broadcast_msg_timer(data, src_host, src_port)
    else:
        pass
    timer = Timer(SEND_INTERVAL, random_send(data, hosts_list))
    timer.start()

def random_data(hosts_list):
    '''
    : random trasfer data
    '''
    trade_double = random.sample(hosts_list, 2)
    return str(trade_double[0]) + ' trasfer * bitcoins to ' \
        + str(trade_double[1]) + '.'

def start_broaccast(hosts_list):
    '''
    : start timer
    '''
    data = random_data(hosts_list)
    print('    25: ' + data)
    timer = Timer(0, random_send(data, hosts_list))
    timer.start()
    return timer
