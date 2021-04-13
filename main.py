import hashlib
import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton
import sys
import os


class Block:

    def __init__(self, bb, previous=None):
        self.bb1 = bb[0]
        self.bb2 = bb[1]
        self.bb3 = bb[2]
        self.bb4 = bb[3]
        self.bb5 = bb[4]
        self.header = BlockHeader(self.bb1, self.bb2, self.bb3, self.bb4, self.bb5, previous)

    def get_hash(self):
        return sha256(self.header)

    def __str__(self):
        return f"No.{self.header.depth}: Merkle root：{self.header.get_hash()}. Here are the transactions: {self.bb1}|" \
               f"{self.bb2}|{self.bb3}|{self.bb4}|{self.bb4}"

    def record(self):
        # Write to the local records.
        pass


class BlockBody:

    def __init__(self, *args):
        argument_length = len(args)
        if argument_length == 3:
            contents = args
        elif argument_length == 1:
            raw = args[0]
            temp = raw.split(",")
            contents = temp
            self.date = contents[3]
        else:
            contents = ["", "", ""]

        if len(contents) == 3:
            self.user_a = contents[0]  # A stands for Alice, the sender.
            self.user_b = contents[1]  # B stands for Bob, the receiver.
            self.transaction_amount = contents[2]
            self.date = datetime.date.today()
        elif len(contents) == 4:
            self.user_a = contents[0]  # A stands for Alice, the sender.
            self.user_b = contents[1]  # B stands for Bob, the receiver.
            self.transaction_amount = contents[2]
            self.date = contents[3]
        else:
            raise IndexError("Not enough information! ")

    def get_hash(self):
        return sha256([self.user_a, self.user_b, self.transaction_amount, self.date])

    def __str__(self):
        return f"{self.user_a}, {self.user_b}, {self.transaction_amount}, {self.date}"


class BlockHeader:

    def __init__(self, bb1, bb2, bb3, bb4, bb5, previous):
        if previous is None:
            self.depth = 1
            self.previous_block_ha = sha256("0")
        else:
            self.depth = previous.depth + 1
            self.previous_block_ha = sha256(previous)
        self.bb1_ha = sha256(bb1)
        self.bb2_ha = sha256(bb2)
        self.bb3_ha = sha256(bb3)
        self.bb4_ha = sha256(bb4)
        self.bb5_ha = sha256(bb5)


    def get_hash(self):
        return sha256([self.bb1_ha, self.bb2_ha, self.bb3_ha, self.bb4_ha, self.bb5_ha, self.previous_block_ha])


def sha256(data: object or str or list) -> object or str:
    """
    The following function does a SHA 256 function to the data and return the value.
    :rtype: str
    :param data: in utf-8 format
    """
    if isinstance(data, object):
        try:
            return data.get_hash()
        except AttributeError:
            temp = hashlib.sha256()
            temp.update(str(data).encode('utf-8'))
            return temp.hexdigest()
    elif isinstance(data, str):
        temp = hashlib.sha256()
        temp.update(data.encode('utf-8'))
        return temp.hexdigest()
    elif isinstance(data, list):
        temp = Tree(data)
        return temp.merkle_root()


class Tree:
    def __init__(self, input_content):

        def copy(data):
            temp = []
            for element in data:
                temp.append(element)
            return temp

        contents = copy(input_content)
        slice_pointer = int(len(contents) / 2 + 0.5)
        while slice_pointer % 2 != 0:
            slice_pointer += 1

        if len(contents) > 2:
            self.left = Tree(copy(contents)[0:slice_pointer])
            self.right = Tree(copy(contents)[slice_pointer:])
        else:
            print(f"Content: {contents}")
            self.left = contents[0]
            try:
                self.right = contents[1]
            except IndexError:
                self.right = contents[0]

    def __str__(self):
        return f"left: ({self.left}); right: ({self.right})"

    def merkle_root(self):
        try:
            return sha256(self.left.merkle_root() + self.right.merkle_root())
        except AttributeError:
            return sha256(sha256(self.left) + sha256(self.right))


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        sender_layout = QHBoxLayout()
        sender_layout.setAlignment(Qt.AlignCenter)
        receiver_layout = QHBoxLayout()
        receiver_layout.setAlignment(Qt.AlignCenter)
        amount_layout = QHBoxLayout()
        amount_layout.setAlignment(Qt.AlignCenter)
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignRight)
        self.label1 = QLabel()
        self.label1.setText("Sender: ")
        self.label2 = QLabel()
        self.label2.setText("Receiver: ")
        self.label3 = QLabel()
        self.label3.setText("Amount: ")
        self.holder1 = QTextEdit()
        self.holder2 = QTextEdit()
        self.holder3 = QTextEdit()
        self.yes = QPushButton()
        self.yes.setText("OK")
        self.yes.clicked.connect(self.make_transaction)
        self.no = QPushButton()
        self.no.setText("Reset")
        self.no.clicked.connect(self.cancel)
        self.currentTransactions = QLabel()
        self.currentTransactions.setText("0")
        sender_layout.addStretch(1)
        sender_layout.addWidget(self.label1)
        sender_layout.addWidget(self.holder1)
        sender_layout.addStretch(1)
        receiver_layout.addStretch(1)
        receiver_layout.addWidget(self.label2)
        receiver_layout.addWidget(self.holder2)
        receiver_layout.addStretch(1)
        amount_layout.addStretch(1)
        amount_layout.addWidget(self.label3)
        amount_layout.addWidget(self.holder3)
        amount_layout.addStretch(1)
        buttons_layout.addWidget(self.no)
        buttons_layout.addWidget(self.yes)
        main_layout = QVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addWidget(self.currentTransactions, 1, Qt.AlignRight)
        main_layout.addLayout(sender_layout)
        main_layout.addLayout(receiver_layout)
        main_layout.addLayout(amount_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addStretch(1)
        main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(main_layout)
        self.blocks = list()

    def make_transaction(self):
        t_file = open("temp.txt", "a")
        block_body = BlockBody(self.holder1.toPlainText(), self.holder2.toPlainText(), self.holder3.toPlainText())
        t_file.write(f"{block_body}\n")
        t_file.close()
        # Add Transaction
        temp = int(self.currentTransactions.text()) + 1
        self.currentTransactions.setText(str(temp))

        if temp >= 5:
            # Make A block
            t_file = open("temp.txt", "r")
            temp = t_file.read().split("\n")
            bb_temp = list()
            for index in range(5):
                bb_temp.append(BlockBody(temp[index]))
            try:
                block_temp = Block(bb_temp, self.blocks[-1])
            except IndexError:
                block_temp = Block(bb_temp)
            self.blocks.append(block_temp)
            self.store_local()

            self.currentTransactions.setText("0")  # Right corner symbol for number of transactions waiting in the pool.

    def cancel(self):
        self.holder1.setText("")
        self.holder2.setText("")
        self.holder3.setText("")

    def import_local(self):
        pass  # read the BlockChain.txt file and import the blocks in.
        # todo Also creates a computer friendly version for local storage thus to import the local blocks. 

    def store_local(self):
        t_file = open("BlockChain.txt", "w")
        for block in self.blocks:
            t_file.write(str(block))
        t_file.close()

    def closeEvent(self, a0) -> None:
        try:
            os.remove("temp.txt")
        except FileNotFoundError:
            pass
        a0.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Window = MainWindow()
    Window.show()
    sys.exit(app.exec_())
