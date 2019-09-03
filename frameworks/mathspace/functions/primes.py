'''
primes.py
'''

def find_primes(n):
    prime_list = [2]
    i = 3
    while len(prime_list) < n:
        for prime in prime_list:
            if i % prime == 0:
                i += 1
                break
        else:
            prime_list.append(i)
            i += 1
    return prime_list