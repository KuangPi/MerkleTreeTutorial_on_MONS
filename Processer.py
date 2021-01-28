"""
Using: Python3.9
This piece of code aim to achieve the following features:
hash with sha256
todo build a Merkle Tree
features of the the merkle tree is included in its description.
"""
import hashlib
import datetime


class Block:
    def __init__(self, user1, user2, money, previous=None):
        """
        The unit of a block chain.
        :param user1:
        :param user2:
        :param money:
        :param previous:
        """
        # todo Init header and body based on information give in one go.
        self.block_body = BlockBody(user1, user2, money)
        self.block_header = BlockHeader(self.block_body, previous)

    def __str__(self):
        return f"\nHeader: \n{self.block_header}\nBody: \n{self.block_body}"

    def __repr__(self):
        return self.__str__()


class BlockBody:
    def __init__(self, user1, user2, money):
        # todo Init the block body.
        """
        Using string to store the information of the users in the transaction
        :param: user1
        :param: user2
        :param
        """
        self.user1 = user1
        self.user2 = user2
        self.money = money

    def __str__(self):
        return f"{self.user1} transfer {self.money} to {self.user2}. Successes. "

    def __repr__(self):
        return f"{self.user1}{self.user2}{self.money}"


class BlockHeader:
    def __init__(self, block_body, previous_block=None):
        if previous_block is None:
            self.number_of_transactions = 1
            self.merkle_root = sha256(block_body.__repr__())
            self.previous_block = None
        else:
            # todo Add the case where is not the first block
            self.number_of_transactions = previous_block.block_header.number_of_transactions + 1
            # todo Change the hash root to merkle root
            self.merkle_root = sha256(block_body.__repr__())
            self.previous_block = previous_block
        # Time stamp seems to be a bit useless since it only reflects the current time.
        self.time_stamp = str(datetime.datetime.today())
        self.hash_root = sha256(block_body.__repr__() + self.__repr__())  # This is dangerous to call repr in init.

    def __str__(self):
        return f"number_of_transactions: {self.number_of_transactions}\n" \
               f"time_stamp: {self.time_stamp}\n" \
               f"merkle_root: {self.merkle_root}\n" \
               f"hash_root: {self.hash_root}"

    def __repr__(self):
        return f"number_of_transactions: {self.number_of_transactions}\n" \
               f"time_stamp: {self.time_stamp}\n" \
               f"merkle_root: {self.merkle_root}\n" \



class MerkleTree:
    def __init__(self, value=None):
        # todo give the values of the merkle tree from the leaf
        self.left_child = MerkleTree()
        self.right_child = MerkleTree()
        if value is None:
            self.value = self.left_child + self.right_child
        else:
            self.value = sha256(value)

    def __add__(self, other):
        return sha256(self.left_child.value + self.right_child.value)


def sha256(data):
    """
    The following function does a SHA 256 function to the data and return the value.
    :param data: in utf-8 format
    :return: str
    """
    temp = hashlib.sha256()
    temp.update(data.encode('utf-8'))
    return temp.hexdigest()


def read_txt(file_name):
    """
    :param file_name: string
    :return:
    """
    file_received = open(file_name, mode="r")
    content = file_received.readlines()
    result = list()
    for element in content:
        element = element[:-1]  # Cut the \n off
        result.append(element.split(" "))
    return result


def create_block_chain_accordingg_to_txt(file_name):
    """
    :param file_name: string
    :return:
    """
    content = read_txt(file_name)
    result = list()
    for element in content:
        if len(element) != 3:
            raise ValueError("Number of information required to build block chain is not enough! 3 each! ")
        else:
            if len(result) == 0:
                result.append(Block(element[0], element[1], int(element[2])))
            else:
                result.append(Block(element[0], element[1], int(element[2]), result[-1]))
    return result


if __name__ == '__main__':
    print(create_block_chain_accordingg_to_txt("ExampleTransactions"))
