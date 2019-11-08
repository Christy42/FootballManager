from random import randint


def repeated_randint(low, high, rolls):
    total = 0
    for i in range(rolls):
        total += randint(low, high)
    return int(total / rolls)
