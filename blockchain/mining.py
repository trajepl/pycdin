import random
from node import PRE_FIX_BLOCK
from block import RAND_NUM, RAND_RANGE

BC_FILE = 'blockchain'


def read_unmark_clear(bcnode):
    """
    : read file unmark and truncate it
    """
    transaction_list = []
    tmp_transactions = bcnode.TRANSACTION
    len_transaction = len(tmp_transactions)

    print('18 mining %s' % bcnode.TRANSACTION)
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
    bcnode.send(PRE_FIX_BLOCK, new_block.bytesstr().decode())


def pow_simulator(rand_number):
    while random.randint(-RAND_RANGE, RAND_RANGE) != rand_number:
            continue  # pow simulator


def run(bcnode):
    while True:
        block_prefix, index_item = bcnode.blockchain.last_block_prefix()
        rand_number = int(block_prefix[RAND_NUM])  # get rand_num of last block
        print('mining 30: %d' %rand_number)
        pow_simulator(rand_number)
        mining(bcnode)
