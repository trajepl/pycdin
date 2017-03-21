import hashlib
import struct
import time
from merkle import Merkle

LEN_PRE_DATA = 148
MAGIC_ID = 0
TIMESTAMP = 1
PREV_HASH = 2
MERKLE_ROOT = 3
LENGTH = 4
DATA = 5
PACK_FORMAT = 'LL64s64sI'
SPLIT_NOTE = '|'

class Block:
    def __init__(self, data, prev_hash, *argv):
        self.magic_id = 0xDAB5BFFA

        # t = time.gmtime(timestamp) time.asctime(t)
        if len(argv) == 0:
            self.timestamp = int(time.time())
        else:
            self.timestamp = argv[0]

        self.prev_hash = prev_hash.encode()
        self.data = list()
        self.set_data(data)  # string of list

        self.length = 0
        self.set_length()
        
        self.merkle_root = None
        if len(argv) == 2:
            self.merkle_root = argv[1].encode()
        else:
            self.set_merkle_root()

    def set_data(self, data):
        self.data = list()
        if isinstance(data, tuple) or isinstance(data, list):
            self.data += data
        else:
            self.data.append(data)

    def print_data(self):
        flag_id = 1
        for d in self.data:
            print('{0:20}: {1}'.format('trade', d)) if flag_id == 1 \
                else print('{0:20}: {1}'.format('', d))
            flag_id += 1
    
    def set_length(self):
        for d in self.data:
            self.length += len(d)

    def set_merkle_root(self):
        mt = Merkle() # default hash: sha256
        mt.add_leaf(self.data, True)
        mt.make_tree()
        self.merkle_root = mt.get_merkle_root().encode()

    def bytesstr(self):
        str_data = ""
        for d in self.data:
            str_data += d + SPLIT_NOTE
        str_data = str_data[:-1]

        pack_format = PACK_FORMAT + str(self.length) + 's'
        return struct.pack(pack_format, self.magic_id, self.timestamp,
                    self.prev_hash, self.merkle_root, self.length, str_data.encode())


    def print_block(self):
        print('{0:20}: {1}'.format('Magic id', hex(self.magic_id)))

        time_format = time.asctime(time.gmtime(self.timestamp))
        print('{0:20}: {1}'.format('timestamp', time_format))

        print('{0:20}: {1}'.format('previous hash', self.prev_hash.decode()))
        print('{0:20}: {1}'.format('merkle_root', self.merkle_root.decode()))
        print('{0:20}: {1}'.format('data length', self.length))
        
        self.print_data()
        print('-' * 86)

if __name__ == '__main__':
    block = Block(['trajep create his', 'a 2 b', 'b 2 c'], '0000000000000000000000000000000000000000000000000000000000000000')
    block.print_block()
