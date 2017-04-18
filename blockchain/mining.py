import time
import random
import struct
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
    bcnode.TRANSACTION = set(list(bcnode.TRANSACTION)[len_transaction:])

    with open(bcnode.UNMARK_FILE, 'w') as tmp: 
        for item in bcnode.TRANSACTION:
            tmp.write(item + '\n')

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
    bcnode.send(PRE_FIX_BLOCK, block_str[:-1])


def pow_simulator(rand_number):
    while random.randint(-RAND_RANGE, RAND_RANGE) != rand_number:
            continue  # pow simulator


def run(bcnode):
    while True:
        block_prefix, index_item = bcnode.blockchain.last_block_prefix()
        rand_number = int(block_prefix[RAND_NUM])  # get rand_num of last block
        print('begin  mining: %d' %rand_number)
        pow_simulator(rand_number)
        mining(bcnode)
        time.sleep(30)
