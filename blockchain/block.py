import time
import struct
import random
import hashlib
from merkle import Merkle

LEN_PRE_DATA = 152
MAGIC_ID = 0
TIMESTAMP = 1
PREV_HASH = 2
MERKLE_ROOT = 3
RAND_NUM = 4
LENGTH = 5
DATA = 6
PACK_FORMAT = 'LL64s64siI' # I: [0, pow(2,32)] i: [-pow(2,32), pow(2,32)]
SPLIT_NOTE = '|'

class Block:
    def __init__(self, data, prev_hash, *argv):
        self.magic_id = 0xDAB5BFFA
        self.prev_hash = prev_hash.encode()
        self.randnum = random.randint(-65535*9999, 65535*9999)

        if len(argv) == 0:
            self.timestamp = int(time.time())
        else:
            self.timestamp = argv[0]  # t = time.gmtime(timestamp) time.asctime(t)

        self.data = list()
        self.set_data(data)  # string of list

        self.length = 0
        self.set_length()
        
        self.merkle_root = None
        if len(argv) == 2:
            self.merkle_root = argv[1].encode()
        else:
            self.set_merkle_root() # ?

    def set_data(self, data):
        '''
        : data: list | string
        '''
        if isinstance(data, tuple) or isinstance(data, list):
            self.data += data
        else:
            self.data.append(data)

    def print_data(self):
        '''
        : format print data information
        '''
        flag_id = 1
        for d in self.data:
            if flag_id == 1:
                print('{0:20}: {1}'.format('trade', d))
            else:
                print('{0:20}: {1}'.format('', d))
            flag_id += 1
    
    def set_length(self):
        for item in self.data:
            self.length += len(item)+1
        self.length -= 1

    def set_merkle_root(self):
        '''
        : make merkle tree and set root
        '''
        mt = Merkle() # default hash: sha256
        mt.add_leaf(self.data, True)
        mt.make_tree()
        self.merkle_root = mt.get_merkle_root().encode()

    def bytesstr(self):
        '''
        : change class(Block) to byte(Block)
        '''
        str_data = ""
        for item in self.data:
            str_data += item + SPLIT_NOTE
        str_data = str_data[:-1]
        self.length = len(str_data)

        pack_format = PACK_FORMAT + str(self.length) + 's'
        print(pack_format)
        return struct.pack(pack_format, self.magic_id, self.timestamp, 
            self.prev_hash, self.merkle_root, self.randnum, self.length, str_data.encode())
                    
    def print_block(self):
        '''
        : format print block information
        '''
        print('{0:20}: {1}'.format('Magic id', hex(self.magic_id)))

        time_format = time.asctime(time.gmtime(self.timestamp))
        print('{0:20}: {1}'.format('timestamp', time_format))

        print('{0:20}: {1}'.format('previous hash', self.prev_hash.decode()))
        print('{0:20}: {1}'.format('merkle_root', self.merkle_root.decode()))
        print('{0:20}: {1}'.format('random number', self.randnum))
        print('{0:20}: {1}'.format('data length', self.length)) # contains split_node
        
        self.print_data()
        print('-' * 86)

if __name__ == '__main__':
    block = Block(['trajep create his', 'a 2 b', 'b 2 c'], '0000000000000000000000000000000000000000000000000000000000000000')
    block.print_block()
