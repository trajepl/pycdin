# broadcast msg
import sys
import time
import random
from threading import Timer

import node

SEND_INTERVAL = 10
TIMER_SEND  = None
   
def random_send(bcnode, data, hosts_list):
    '''
    : set fixed time (interval 10s) to randomly selectting a source host sending data
    '''
    is_continue = random.choice([True, False])
    if is_continue :
        src_hosts = random.choice(hosts_list)
        src_host = src_hosts[0]
        src_port = src_hosts[1]
        print('DEBUG 17 src_hosts: ' + str(src_hosts))
        bcnode.send(node.PRE_FIX_TRANSACTION, data)
    else:
        pass
    
    global TIMER_SEND
    TIMER_SEND = Timer(SEND_INTERVAL, random_send(bcnode, data, hosts_list))
    TIMER_SEND.start()

def random_data(hosts_list):
    '''
    : trasfaction data
    '''
    trade_double = random.sample(hosts_list, 2)
    return str(trade_double[0]) + ' trasfer * bitcoins to ' \
        + str(trade_double[1]) + '.'

def send(bcnode, hosts_list):
    '''
    : start timer
    '''
    data = random_data(hosts_list)
    print('DEBUG 25 data: ' + data)

    global TIMER_SEND
    TIMER_SEND = Timer(0, random_send(bcnode, data, hosts_list))
    TIMER_SEND.start()


# # test
# if __name__ == '__main__':
#     hosts_list = [('127.0.0.1', 9000), ('127.0.0.1', 9001), ('127.0.0.1', 9002), ('127.0.0.1', 9003)]
#     send(hosts_list)

#     time.sleep(15)
#     timer.cancle()