import heapq

class LCV_Var:
    def __init__(self, value, const_count):
        self.value = value
        self.const_count = const_count

    def __lt__(self, other):
        return other.const_count > self.const_count

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

