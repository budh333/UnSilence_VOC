import math

def is_square(n):
    sqrt = math.sqrt(n)
    return (sqrt - int(sqrt)) == 0

def get_square(n):
    sqrt = math.sqrt(n)
    return int(sqrt)