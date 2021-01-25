"""
Using: Python3.9
This piece of code aim to achieve the following features:
hash with sha256
todo build a Merkle Tree
features of the the merkle tree is included in its description.
"""


# Features of this script might not be used.
# todo Develop the processor first


class User:
    """
    People transaction their money
    """
    def __init__(self):
        self.money = 0
        self.transaction_passed = list()

    def transaction(self, other, money):
        return Transaction(self, other, money)


class Transaction:
    """
    Represents the transaction occurs.
    """
    def __init__(self, userA, userB, money):
        """
        :param userA: type User
        :param userB: type User
        """
        self.userA = userA
        self.userB = userB
        self.money = money


if __name__ == '__main__':
    pass
