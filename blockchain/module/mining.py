# broadcast msg
import sys
import random
from threading import Timer

from chain import RAND_NUM

UNMARK_FILE = 'unmark'
BC_FILE = 'blockchain'

def mining():    
    transaction_list = read_unmark_clear(UNMARK_FILE)
    bc = chain.Chain()
    bc.add_block(trade,  'blockchain')

def read_unmark_clear(fn):
    '''
    : read file unmark and truncate it
    '''
    transaction_list = []
    with open(fn, 'r') as transfer_out:
        while True:
            tmp = transfer_out.readline()
            break if tmp is None else transaction_list.append(tmp)
        transfer_out.seek(0)
        transfer_out.truncate()
    return transaction_list

def run():
    blockchain = chain.Chain()
    block_prefix, index_item = blockchain.last_block_prefix(BC_FILE)
    rand_number = int(block_prefix[RAND_NUM]) # get rand_num of last block

    while(random.randint(-65535*9999, 65535*9999) != rand_number)
        continue # pow simulator

    mining()
