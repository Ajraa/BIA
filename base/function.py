class Function:
    def __init__(self, func, name, bounds, points):
        self.func = func
        self.name = name
        self.bounds = bounds 
        self.points = points

    def do(self, x, y):
        return self.func([x, y])
    
    def do(self, x):
        return self.func(x)