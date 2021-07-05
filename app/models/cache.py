from app.services.errorService import ErrorHandler
from app.models.block import Block


class Cache:

    def __init__(self, capacity):
        if capacity <= 1:
            raise ErrorHandler("Capacity cannot be less than or equal to 1!", status_code=400)

        self.head = Block("head", None)
        self.tail = Block("tail", None)
        self.data = {}
        self.__blocks = {}
        self.head.next_block = self.tail
        self.tail.prev_block = self.head
        self.__capacity = capacity
        self.__size = 0

    # Only used for testing
    def get_capacity(self):
        return self.__capacity

    # Only used for testing
    def get_size(self):
        return self.__size

    # Only used for testing
    def set_size(self, size):
        self.__size = size

    # Only used for testing
    def get_blocks(self):
        return self.__blocks

    # Only used for testing
    def add_block_data_to_blocks(self, block):
        self.__blocks[block.number] = block

    def is_full(self):
        return self.__size == self.__capacity

    def get_head(self):
        if self.__size > 0:
            return self.head.next_block
        return None

    def remove_block(self, block):
        if self.__size == 0:
            raise ErrorHandler("Cannot remove block from an empty cache!")

        block.prev_block.next_block = block.next_block
        block.next_block.prev_block = block.prev_block
        del self.data[block.number]
        del self.__blocks[block.number]
        self.__size -= 1

    def remove_tail(self):
        if self.__size <= 1:
            raise ErrorHandler("You cannot remove a tail from cache with size equal to or less than 1!")
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
        self.__blocks[block.number] = block
        self.__size += 1

    def move_to_head(self, block):
        self.remove_block(block)
        self.add_to_head(block)

    def get_block_by_number(self, number):
        if number in self.__blocks:
            return self.__blocks[number]
        return None
