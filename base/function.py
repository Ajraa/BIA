class Function:
    def __init__(self, func, name, lower_bound, upper_bound, points):
        self.func = func
        self.name = name
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.points = points

    def do(self, x, y):
        return self.func([x, y])