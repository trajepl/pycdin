# broadcast msg
import sys
import time
import random
from threading import Timer

import trade

SEND_INTERVAL = 10
TIMER_SEND  = None

def broadcast_msg(data, host, port):
    '''
    : (host, port) broadcasts trasfer data to its first-step node.
    '''
    send_process = trade.Trade(host, int(port))
    send_process.send(data)
   
def random_send(data, hosts_list):
    '''
    : set fixed time (interval 10s) to randomly selectting a source host sending data
    '''
    is_continue = random.choice([True, False])
    if is_continue :
        src_hosts = random.choice(hosts_list)
        src_host = src_hosts[0]
        src_port = src_hosts[1]
        print('DEBUG 17 src_hosts: ' + str(src_hosts))
        broadcast_msg(data, src_host, src_port)
    else:
        pass
    
    global TIMER_SEND
    TIMER_SEND = Timer(SEND_INTERVAL, random_send(data, hosts_list))
    TIMER_SEND.start()

def random_data(hosts_list):
    '''
    : random trasfer data generator
    '''
    trade_double = random.sample(hosts_list, 2)
    return str(trade_double[0]) + ' trasfer * bitcoins to ' \
        + str(trade_double[1]) + '.'

def start_broadcast(hosts_list):
    '''
    : start timer
    '''
    data = random_data(hosts_list)
    print('DEBUG 25 data: ' + data)

    global TIMER_SEND
    TIMER_SEND = Timer(0, random_send(data, hosts_list))
    TIMER_SEND.start()


# call by 'python broadcast hosts_list1 hosts_list2 ...'
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("error param.")
    else:
        hosts_list = sys.argv[1:]
        start_broadcast(hosts_list)



# # test
# if __name__ == '__main__':
#     hosts_list = [('127.0.0.1', 9000), ('127.0.0.1', 9001), ('127.0.0.1', 9002), ('127.0.0.1', 9003)]
#     start_broadcast(hosts_list)

#     time.sleep(15)
#     timer.cancle()