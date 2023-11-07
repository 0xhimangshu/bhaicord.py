import random


class Color:

    @staticmethod
    def random() -> int:
        """Gets a random number for discord color"""
        return random.randint(0, 0xFFFFFF)

    @staticmethod
    def black() -> int:
        return 0