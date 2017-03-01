import hashlib
import struct
import time

class Block:
    def __init__(self, data, prev_hash):
        self.magic_id = 0xDAB5BFFA

        # t = time.gmtime(timestamp) time.asctime(t)
        self.timestamp = int(time.time())

        self.prev_hash = prev_hash.encode()
        self.data = data.encode()
        self.length = len(self.data)

        self.hash_value = hashlib.sha256(self.data).hexdigest().encode()


    def bytesstr(self):
        pack_format = 'LL64s64sI' + str(self.length) + 's'
        return struct.pack(pack_format, self.magic_id, self.timestamp,
                    self.prev_hash, self.hash_value, self.length, self.data)


    def print_block(self):
        print('{0:20}: {1}'.format('Magic id', hex(self.magic_id)))

        time_format = time.asctime(time.gmtime(self.timestamp))
        print('{0:20}: {1}'.format('timestamp', time_format))

        print('{0:20}: {1}'.format('previous hash', self.prev_hash.decode()))
        print('{0:20}: {1}'.format('hash_value', self.hash_value.decode()))
        print('{0:20}: {1}'.format('data length', self.length))
        print('{0:20}: {1}'.format('data', self.data.decode()))

if __name__ == '__main__':
    block = Block('trajep create his', '0000000000000000000000000000000000000000000000000000000000000000')
    block.print_block()