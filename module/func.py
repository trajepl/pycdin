# module

import random

def rand_num(x):   
    if len(x) == 0: 
        x = 10
    else:
        x = int(x[0])
    return random.randint(0, 1000) % x

run = rand_num
