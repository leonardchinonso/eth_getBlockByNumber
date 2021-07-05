from app.services.errorService import ErrorHandler
from app.models.block import Block


class Cache:

    def __init__(self, capacity):
        if capacity <= 1:
            raise ErrorHandler("Capacity cannot be less than 1", status_code=400)

        self.head = Block("head", None)
        self.tail = Block("tail", None)
        self.data = {}
        self.blocks = {}
        self.head.next_block = self.tail
        self.tail.prev_block = self.head
        self.capacity = capacity
        self.size = 0

    def is_full(self):
        return self.size == self.capacity

    def get_head(self):
        if self.size > 0:
            return self.head.next_block
        return None

    def remove_block(self, block):
        block.prev_block.next_block = block.next_block
        block.next_block.prev_block = block.prev_block
        del self.data[block.number]
        del self.blocks[block.number]
        self.size -= 1

    def remove_tail(self):
        if self.size == 1:
            raise ErrorHandler("You cannot remove a tail from cache with size 1")
        self.remove_block(self.tail.prev_block)

    def add_to_head(self, block):
        if self.is_full():
            self.remove_tail()

        temp = self.head.next_block
        self.head.next_block = block
        block.prev_block = self.head
        block.next_block = temp
        temp.prev_block = block
        self.data[block.number] = block.data
        self.blocks[block.number] = block
        self.size += 1

    def move_to_head(self, block):
        self.remove_block(block)
        self.add_to_head(block)

    def get_block_by_number(self, number):
        if number in self.blocks:
            return self.blocks[number]
        return None
