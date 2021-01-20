"""
Using: Python3.9
This piece of code aim to achieve the following features:
hash with sha256
todo build a Merkle Tree
features of the the merkle tree is included in its description.
"""
import hashlib


class MerkleTree:
    """
    This Merkle tree should be able to do the following things:

    """
    def __init__(self,
                 number_of_transactions=0,
                 height=0,
                 block_reward=1,
                 time_stamp=0,
                 merkle_root=None,
                 previous_block=0,
                 difficulty=0,
                 bits=0,
                 size=0,
                 version=0,
                 nonce=0,
                 next_block=0):
        self.number_of_transactions = number_of_transactions
        self.height = height
        self.block_reward = block_reward
        self.time_stamp = time_stamp
        self.merkle_root = merkle_root
        self.previous_block = previous_block
        self.difficulty = difficulty
        self.bits = bits
        self.size = size
        self.version = version
        self.nonce = nonce
        self.next_block = next_block

    def __str__(self):
        temp = f"number_of_transactions: {self.number_of_transactions}\n" \
               f"height: {self.height}\n" \
               f"block_reward: {self.block_reward}\n" \
               f"time_stamp: {self.time_stamp}\n" \
               f"merkle_root: {self.merkle_root}\n" \
               f"prebious_block: {self.previous_block}\n" \
               f"difficulty: {self.difficulty}\n" \
               f"bits: {self.bits}\n" \
               f"size: {self.size}\n" \
               f"version: {self.version}\n" \
               f"nonce: {self.nonce}\n" \
               f"next_block: {self.next_block}"

        return temp


def sha256(data):
    """
    The following function does a SHA 256 function to the data and return the value.
    :param data: in utf-8 format
    :return: str
    """
    temp = hashlib.sha256()
    temp.update(data.encode('utf-8'))
    return temp.hexdigest()


if __name__ == '__main__':
    test = MerkleTree()
    print(test)