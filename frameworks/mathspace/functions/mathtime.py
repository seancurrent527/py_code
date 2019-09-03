'''
mathtime.py
'''

import time

def find_time(func, n):
    t1 = time.time()
    func(n)
    t2 = time.time()
    return t2 - t1