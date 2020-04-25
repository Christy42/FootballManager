from copy import deepcopy
from random import randint, choices, random


def repeated_randint(low, high, rolls):
    total = 0
    for i in range(rolls):
        total += randint(low, high)
    return int(total / rolls)


def repeated_random(number: int, odds: float) -> int:
    total = 0
    for i in range(number):
        total = total + 1 if random() > odds else 0
    return total


def combine_values(listed, weights=(10, 8, 6, 4, 3, 2, 1, 1, 1, 1, 1)):
    sum_value = sum(weights)
    copy_list = deepcopy(listed)
    new_list = []
    for i in range(len(listed)):
        new_list.append(max(copy_list) * weights[i] / sum_value)
        copy_list.remove(max(copy_list))
    return sum(new_list)


def get_pos(cur_list, rota):
    counter = 0
    while True:
        wr4 = choices(list(rota.keys()), weights=list(rota.values()))
        counter += 1
        if wr4 not in cur_list:
            return wr4
        if counter > 1000:
            print("No value possible in {}".format(rota))
            return 0


def exp_limited(lower_bound, upper_bound, exp=2):
    listed_values = [upper_bound]
    number = 1
    for i in range(upper_bound-1, lower_bound, -1):
        number *= exp
        listed_values += [i] * round(number)
    return listed_values[randint(0, len(listed_values)-1)]
