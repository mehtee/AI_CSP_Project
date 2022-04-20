import heapq

class MRV_Var:
    def __init__(self, cell, const_count):
        self.cell = cell
        self.const_count = const_count

    def __lt__(self, other):
        return other.const_count < self.const_count

    def __repr__(self):
        return str(self.cell) + " " + str(self.const_count)
