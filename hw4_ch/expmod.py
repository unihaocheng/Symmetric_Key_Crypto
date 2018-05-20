# Author: Hao CHENG
# Date: 19th Mar 2018
# Description: Modular exponentiation of small integers


import sys

num_a = int(sys.argv[1])
num_b = int(sys.argv[2])
num_mod = int(sys.argv[3])


def mod_exp(a, b, mod):
    bin_b = bin(b)
    c = 1
    for i in range(2, len(bin_b)):
        c = (c * c) % mod
        if bin_b[i] == '1':
            c = (c * a) % mod
    return c


if __name__ == '__main__':
    print (mod_exp(num_a, num_b, num_mod))
