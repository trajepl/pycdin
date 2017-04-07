# broadcast msg
import sys
import random
import chain

from block import RAND_NUM

BC_FILE = 'blockchain'

def mining(bcnode):    
    transaction_list = read_unmark_clear(bcnode)
    bcnode.blockchain.add_block(trade)

def read_unmark_clear(bcnode):
    '''
    : read file unmark and truncate it
    '''
    transaction_list = []
    
    for item in bcnode.TRANSACTION:
        transaction_list.append(item)
    bcnode.TRANSACTION = []
    with open(bcnode.UNMARK_FILE, 'w') as tmp: pass
    return transaction_list

def run(bcnode):
    while True:
        block_prefix, index_item = bcnode.blockchain.last_block_prefix()
        rand_number = int(block_prefix[RAND_NUM]) # get rand_num of last block

        while random.randint(-65535*9999, 65535*9999) != rand_number:
            continue # pow simulator

        mining(bcnode)
