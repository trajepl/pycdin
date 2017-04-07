import struct
from block import Block, LEN_PRE_DATA, SPLIT_NOTE, \
    PREV_HASH, MERKLE_ROOT, LENGTH, PACK_FORMAT, TIMESTAMP

ITEM_LEN = 16 # index file length

class Chain:
    def __init__(self, port):
        self.blockchain = []
        self.index_file = 'bcinfo/' + str(port) + '/index.id'
        self.bc_file = 'bcinfo/' + str(port) + '/blockchain'

    def write_block(self, block, open_way):
        with open(self.bc_file, open_way) as chain:
            chain.write(block.bytesstr())

    def update_index(self, index_item, open_way):
        item = struct.pack('QQ', index_item[0], index_item[1])
        with open(self.index_file, open_way) as index:
            index.write(item)

    def create_first_block(self, data):
        block = Block(data, '0000000000000000000000000000000000000000000000000000000000000000')
        self.write_block(block, 'wb')

        # update index file
        index_item = [0, 0]
        self.update_index(index_item, 'wb')

        index_item[0] += 1
        index_item[1] = block.length + LEN_PRE_DATA
        self.update_index(index_item, 'ab')

    def read_chain(self):
        with open(self.bc_file, 'rb') as chain:
            while True:
                # read block prefix
                block_bytes = chain.read(LEN_PRE_DATA)
                if len(block_bytes) < LEN_PRE_DATA:
                    break

                block = list(struct.unpack(PACK_FORMAT, block_bytes))
                data_len = block[LENGTH]
                prev_hash = block[PREV_HASH].decode()
                merkle_root = block[MERKLE_ROOT].decode()
                timestamp = block[TIMESTAMP]

                # read block data
                data_bytes = chain.read(data_len)
                data = struct.unpack(str(data_len) + 's', data_bytes)[0].decode()
                data = data.split(SPLIT_NOTE)

                block.append(data)
                self.blockchain.append(Block(data, prev_hash, timestamp, merkle_root))

    def print_chain(self):
        for block in self.blockchain:
            block.print_block()

    def last_block_prefix(self):
        index_item = []
        with open(self.index_file, 'rb') as index:
            index.seek(-32, 2)
            index_item_bytes1 = index.read(ITEM_LEN)
            index_item.append(list(struct.unpack('QQ', index_item_bytes1)))
            index_item_bytes2 = index.read(ITEM_LEN)
            index_item.append(list(struct.unpack('QQ', index_item_bytes2)))

        with open(self.bc_file, 'rb') as chain:
            chain.seek(index_item[0][1], 0)
            block_bytes = chain.read(LEN_PRE_DATA)
            block = list(struct.unpack(PACK_FORMAT, block_bytes))
            block[MERKLE_ROOT] = block[MERKLE_ROOT].decode()

        return block, index_item[1]

    def new_block(self, data):
        with open(self.index_file, 'rb') as index:
            index.seek(-32, 2)
            index_item_bytes = index.read(ITEM_LEN)
            index_item = struct.unpack('QQ', index_item_bytes)

        with open(self.bc_file, 'rb') as chain:
            chain.seek(index_item[1], 0)
            block_bytes = chain.read(LEN_PRE_DATA)
            block = struct.unpack(PACK_FORMAT, block_bytes)

            prev_hash = block[MERKLE_ROOT].decode()
            return Block(data, prev_hash)

    def push_chain(self, data):
        block_prefix, index_item = self.last_block_prefix()
        prev_hash = block_prefix[MERKLE_ROOT]
        timestamp = block_prefix[TIMESTAMP]
        block = Block(data, prev_hash, timestamp)
        self.blockchain.append(block)
        return block

    def add_block(self, data):
        block_prefix, index_item = self.last_block_prefix()
        prev_hash = block_prefix[MERKLE_ROOT]
        block = Block(data, prev_hash)
        self.write_block(block, 'ab')

        # update index file 
        len_block = block.length + LEN_PRE_DATA
        index_item[0] += 1
        index_item[1] += len_block
        self.update_index(index_item, 'ab')

    def print_index(self):
        index_list = []
        with open(self.index_file, 'rb') as index:
            while True:
                index_item_bytes = index.read(ITEM_LEN)
                if len(index_item_bytes) < ITEM_LEN:
                    break
                index_item = struct.unpack('QQ', index_item_bytes)
                index_list.append(index_item)
        print(index_list)


if __name__ == '__main__':
    chain = Chain(9000)
    trade = ["trajep2 create first block.", "trajep create 2rd block.", "trajep create 3th block."]
    chain.create_first_block('trajep create first block.')

    # chain.add_block(trade)

    chain.read_chain()

    # chain.push_chain('trajep create 4th block.')

    chain.print_chain()
    chain.print_index()
