from typing import Optional


class Block:

    def __init__(self, number: str, data: Optional[dict], prev_block=None, next_block=None):
        self.number = number
        self.data = data
        self.prev_block = prev_block
        self.next_block = next_block

    def get_next_block(self):
        return self.next_block

    def set_next_block(self, next_block=None):
        self.next_block = next_block

    def get_prev_block(self):
        return self.prev_block

    def set_prev_block(self, prev_block=None):
        self.prev_block = prev_block

