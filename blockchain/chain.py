import struct
from block import Block, LEN_PRE_DATA, \
    PREV_HASH, HASH_VALUE, LENGTH, PACK_FORMAT

ITEM_LEN = 16
class Chain:
    def __init__(self):
        self.blockchain = []

    def write_block(self, block, fn, open_way):
        with open(fn, open_way) as chain:
            chain.write(block.bytesstr())

    def update_index(self, index_item, fn, open_way):
        item = struct.pack('QQ', index_item[0], index_item[1])
        with open(fn, open_way) as index:
            index.write(item)

    def create_first_block(self, data, fn):
        block = Block(data, '0000000000000000000000000000000000000000000000000000000000000000')
        self.write_block(block, fn, 'wb')

        # update index file 'index.id'
        index_item = [0, 0]
        self.update_index(index_item, 'index.id', 'wb')

        index_item[0] += 1
        index_item[1] = len(data) +  LEN_PRE_DATA
        self.update_index(index_item, 'index.id', 'ab')

    def read_chain(self, fn):
        with open(fn, 'rb') as chain:
            while True:
                # read block prefix
                block_bytes = chain.read(LEN_PRE_DATA)
                if len(block_bytes) < LEN_PRE_DATA:
                    break

                block = list(struct.unpack(PACK_FORMAT, block_bytes))
                data_len = block[LENGTH]
                prev_hash = block[HASH_VALUE].decode()

                # read block data
                data_bytes = chain.read(data_len)
                data = struct.unpack(str(data_len) + 's', data_bytes)[0].decode()

                block.append(data)
                self.blockchain.append(Block(data, prev_hash))

    def print_chain(self):
        for block in self.blockchain:
            block.print_block()

    def last_block_prefix(self, fn):
        index_item = []
        with open('index.id', 'rb') as index:
            index.seek(-32, 2)
            index_item_bytes1 = index.read(ITEM_LEN)
            index_item.append(list(struct.unpack('QQ', index_item_bytes1)))
            index_item_bytes2 = index.read(ITEM_LEN)
            index_item.append(list(struct.unpack('QQ', index_item_bytes2)))

        with open(fn, 'rb') as chain:
            chain.seek(index_item[0][1], 0)
            block_bytes = chain.read(LEN_PRE_DATA)
            block = list(struct.unpack(PACK_FORMAT, block_bytes))
            block[HASH_VALUE] = block[HASH_VALUE].decode()

        return block, index_item[1]


    def new_block(self, data, fn):
        with open('index.id', 'rb') as index:
            index.seek(-32, 2)
            index_item_bytes = index.read(ITEM_LEN)
            index_item = struct.unpack('QQ', index_item_bytes)

        with open(fn, 'rb') as chain:
            chain.seek(index_item[1], 0)
            block_bytes = chain.read(LEN_PRE_DATA)
            block = struct.unpack(PACK_FORMAT, block_bytes)

            prev_hash = block[HASH_VALUE].decode()
            return Block(data, prev_hash)


    def push_chain(self, data, fn):
        block_prefix, index_item = self.last_block_prefix(fn)
        prev_hash = block_prefix[HASH_VALUE]
        block = Block(data, prev_hash)
        self.blockchain.append(block)
        return block


    def add_chain(self, data, fn):
        block_prefix, index_item = self.last_block_prefix(fn)
        prev_hash = block_prefix[HASH_VALUE]
        block = Block(data, prev_hash)
        self.write_block(block, fn, 'ab')

        # update index file 'index.id'
        len_block = block_prefix[LENGTH] + LEN_PRE_DATA
        index_item[0] += 1
        index_item[1] += len_block
        self.update_index(index_item, 'index.id', 'ab')


    def print_index(self, fn):
        index_list = []
        with open(fn, 'rb') as index:
            while True:
                index_item_bytes = index.read(ITEM_LEN)
                if len(index_item_bytes) < ITEM_LEN:
                    break
                index_item = struct.unpack('QQ', index_item_bytes)
                index_list.append(index_item)
        print(index_list)

if __name__ == '__main__':
    chain = Chain()
    chain.create_first_block('trajep create first block.', 'blockchain')

    # chain.add_chain( 'trajep create 2rd block.', 'blockchain')

    # chain.push_chain('trajep create 2rd block.', 'blockchain')
    # chain.push_chain('trajep create 3th block.', 'blockchain')

    chain.read_chain('blockchain')
    chain.print_chain()
    chain.print_index('index.id')





