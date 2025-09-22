import math

def sphere(input):
    return sum(x**2 for x in input)

def ackley(input, a=20, b=0.2, c=2*math.pi):
    d = len(input)

    sum1 = sum(x**2 for x in input)
    term1 = -a * math.exp(-b * math.sqrt(sum1/d))
    
    sum2 = sum(math.cos(c*x) for x in input)
    term2 = -math.exp(sum2/d)

    return term1 + term2 + a + math.exp(1)

def rastrigin(input):
    d = len(input)
    term = sum(x**2 - 10 * math.cos(2 * math.pi * x) for x in input)
    return 10 * d + term

def rosenbrock(input):
    return sum(100 * (input[i+1] - input[i]**2)**2 + (input[i] - 1)**2 for i in range(len(input) - 1))

def griewank(input):
    term = sum(x**2/4000 for x in input)
    product = math.prod(math.cos(input[i]/math.sqrt(i+1)) for i in range(len(input)))
    return 1 + term - product

def schwefel(input):
    return 418.9829 * len(input) - sum(x * math.sin(math.sqrt(abs(x))) for x in input)

def levy(input):
    w = [1 + (x - 1) / 4 for x in input]
    d = len(input)

    term1 = math.sin(math.pi * w[0])**2
    term2 = sum((w[i] - 1)**2 * (1 + 10 * math.sin(math.pi * w[i] + 1)**2) for i in range(d - 1))
    term3 = (w[-1]-1)**2 * (1 + math.sin(2 * math.pi * w[-1])**2)

    return term1 + term2 + term3

def michalewicz(input, m=10):
    return -sum(math.sin(input[i]) * math.sin(((i+1) * input[i]**2) / math.pi)**(2*m) for i in range(len(input)))

def zakharov(input):
    d = len(input)

    sum1 = sum(x**2 for x in input)
    sum2 = sum(0.5 * (i+1) * input[i] for i in range(d))**2
    sum3 = sum(0.5 * (i+1) * input[i] for i in range(d))**4

    return sum1 + sum2 + sum3