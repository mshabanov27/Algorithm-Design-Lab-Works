class DatabaseObject:
    def __init__(self, index, value):
        self.__index = index
        self.__value = value

    def __lt__(self, other):
        return self.value < other

    def __gt__(self, other):
        return self.value > other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    @property
    def value(self):
        return self.__value

    @property
    def index(self):
        return self.__index
