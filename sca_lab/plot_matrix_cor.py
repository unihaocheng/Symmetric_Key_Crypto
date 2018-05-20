# Author: Hao CHENG
# Date: 16th May 2018

import matplotlib.pyplot as plt
import numpy as np
import os


input_dir = "./output"

key = [127, 109, 38, 207, 255, 251, 172, 28, 165, 25, 117, 63, 211, 136, 196, 205]


def load(filepath):
    '''Load a numpy array from ${filepath}.npy'''
    return np.load(filepath + ".npy")


Cs = load(os.path.join(input_dir, "correlation_matrices"))


def plot_graph(Cs):
    plt.ylabel("Correlation")
    plt.xlabel("Sample Points")

    for i in range(0, 16):
        Cs_one_byte = Cs[i]
        plt.figure()
        for k in range(0, 256):
            if k == key[i]:
                plt.plot(np.abs(Cs_one_byte[k]), 'y')
            else:
                plt.plot(np.abs(Cs_one_byte[k]), 'b')
        plt.savefig("./output/byte_%s.png" % i)


if __name__ == "__main__":
    plot_graph(Cs)
