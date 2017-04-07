import random

from block import RAND_NUM, RAND_RANGE

BC_FILE = 'blockchain'


def mining(bcnode):
    transaction_list = read_unmark_clear(bcnode)
    bcnode.blockchain.add_block(transaction_list)


def read_unmark_clear(bcnode):
    """
    : read file unmark and truncate it
    """
    transaction_list = []
    print('18 mining %s' % bcnode.TRANSACTION)
    for item in bcnode.TRANSACTION:
        transaction_list.append(item)
    bcnode.TRANSACTION = set()
    with open(bcnode.UNMARK_FILE, 'w') as tmp: pass
    return transaction_list


def run(bcnode):
    while True:
        block_prefix, index_item = bcnode.blockchain.last_block_prefix()
        rand_number = int(block_prefix[RAND_NUM])  # get rand_num of last block
        print('mining 30: %d' %rand_number)
        while random.randint(-RAND_RANGE, RAND_RANGE) != rand_number:
            continue  # pow simulator

        mining(bcnode)
