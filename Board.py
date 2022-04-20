from copy import deepcopy

class Board:
    def __init__(self, state, domains, assigned_variable = None, assigned_value = None, old = None):
        self.state = deepcopy(state)
        self.domains = deepcopy(domains)
        self.assigned_variable = assigned_variable
        self.assigned_value = assigned_value
        self.old = old