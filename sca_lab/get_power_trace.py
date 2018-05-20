# Author: Hao CHENG
# Date: 15th May 2018

import driver
import discovery
import numpy as np
import random
import os
import aes_sbox
import aes_encrypt
import tqdm


target_use = driver.Driver()
scope_use = discovery.Discovery()
scope_use.setMode("normal")
scope_use.enableChannel(0)
scope_use.enableChannel(1)
scope_use.setTriggerEdge(1, 2, "rising")
scope_use.run()


min_length_arr = lambda samples: len(min(samples, key=lambda x: len(x)))


# Assignment 5.2
def generateRandomPlaintext():
    return random.getrandbits(128)


# Assignment 5.1
def encryptPlaintext(target, plaintext):
        ciphertext = target.encrypt(plaintext)
        return ciphertext


# Assignment 5.3
def measureCurrent(scope, target, plaintext, num=4000):
    scope.run()
    while not scope.isReady():
        target.encrypt(plaintext)
    channet = scope.getSamples(0)[:num]
    trigersig = scope.getSamples(1)[:num]
    begin, end = gam(trigersig)
    return channet[begin:end]


def gam(samples):
    filtered = [(n, x) for n, x in enumerate(samples) if x > 2.0]
    return (filtered[0][0], filtered[-1][0])


# Assignment 6.2
def save(arr, output_dir, output_file):
    '''Saves an array at ${output_dir}/${output_file}'''
    path = os.path.join(output_dir, output_file)
    np.save(path, arr)


def getTraces(trace_num, output_dir):
    T, M = measure(scope_use, target_use, trace_num)
    save(T, output_dir, "plaintext_matrix")
    save(M, output_dir, "trace_matrix")
    return T, M


# Assignment 6.1
def measure(scope, target, num_pt):
    T = []
    M = []
    for _ in tqdm.trange(num_pt):
        plaintext = generateRandomPlaintext()
        T += [plaintext]
        M += [currentAvg(scope, target, plaintext, iters=8)]
    return np.array(T), truncateMatrix(M)


def plotCurrentWaveform(samples):
    plt.plot(samples)
    plt.show()


def currentAvg(scope, target, data, num=4000, iters=8):
    samples = [measureCurrent(scope, target, data, num) for _ in xrange(iters)]
    return np.mean(truncateMatrix(samples), axis=0)


def truncateMatrix(samples):
    min_length = min_length_arr(samples)
    return np.array(map(lambda x: x[:min_length], samples))


if __name__ == '__main__':
    trace_number = 500
    output_dir = "./output"

    print "Getting the power traces now"
    print "\n********************************************\n"
    print "Number of power traces:", trace_number
    print "Output directory:", output_dir
    print "\n********************************************\n"
    getTraces(trace_number, output_dir)
    print "Finished!"
    target_use.close()
    scope_use.close()
