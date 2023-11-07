class SizeOutOfBounds(Exception):

    def __init__(self):
        super().__init__("the maximum is 4069 and the minimum is 16")


class ClientNotFound(Exception):

    def __init__(self):
        super().__init__("Client instance wasn't found")