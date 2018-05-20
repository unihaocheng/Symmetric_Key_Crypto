# Author: Hao CHENG
# Data: 15th May 2018

import os
import functools
import scipy.stats as scipy
import numpy as np
import aes_sbox
import multiprocessing


hamming_weight = lambda x: bin(x).count('1')
select_byte    = lambda num, byte: (num & (0xFF << (8 * byte))) >> (8 * byte)
to_hex = lambda x: hex(x)[2:].rstrip('L').zfill(2).upper()


# Assignment 6.2
def save(arr, output_dir, output_file):
    '''Saves an array at ${output_dir}/${output_file}'''
    path = os.path.join(output_dir, output_file)
    np.save(path, arr)


# Assignment 6.3
def load(filepath):
    '''Load a numpy array from ${filepath}.npy'''
    return np.load(filepath + ".npy")


input_dir = "./output"
T = load(os.path.join(input_dir, "plaintext_matrix"))
M = load(os.path.join(input_dir, "trace_matrix"))


# Assignment 6.4
def predictCurrent(key_byte, plaintext_byte):
    return hamming_weight(aes_sbox.SBOX[key_byte ^ plaintext_byte])


# Assignment 6.5
def generatePredictedCurrents(T, byte_idx):
    P = np.zeros((len(T), 256))
    for n, p in enumerate(T):
        p_selected = select_byte(p, byte_idx)
        for key in xrange(256):
            P[n][key] = predictCurrent(key, p_selected)
    return P


# Assignment 6.6
def calculatePearsonCoefficient(x_arr, y_arr):
    x_mean = np.mean(x_arr)
    y_mean = np.mean(y_arr)
    numerator = sum([(x - x_mean) * (y - y_mean) for (x, y) in zip(x_arr, y_arr)])
    delta_1 = sum([(x - x_mean) ** 2 for x in x_arr])
    delta_2 = sum([(y - y_mean) ** 2 for y in y_arr])
    return (numerator) / math.sqrt(delta_1 * delta_2)


# Assignment 6.7
def computeC(P, M):
    '''compute matrix C'''
    sample_num = M.shape[1]
    C = np.empty((256, sample_num))
    for key in xrange(256):
        for s_idx in xrange(sample_num):
            C[key][s_idx] = scipy.pearsonr(P[:, key], M[:, s_idx])[0]
    return C


def all_pearson_matrices(T, M, n_jobs=1):
    repeat = map
    func = functools.partial(calculate_pearson_matrix, T, M)
    if n_jobs > 1:
        repeat = multiprocessing.Pool(n_jobs).map

    return repeat(func, range(16))


def calculate_pearson_matrix(T, M, byte_idx):
    P = generatePredictedCurrents(T, byte_idx)
    C = computeC(P, M)
    print "Correlation calculation for byte %s finished!" % byte_idx
    return C


# Assignment 6.9
def findKey(C_Matrix):
    key = []
    for c in C_Matrix:
        key.append(np.unravel_index(np.argmax(np.abs(c)), c.shape)[0])
    return key


if __name__ == "__main__":
    print "\nThe Program of CPA Attack"
    print "\n********************************************\n"
    print "The directory of power traces:", input_dir
    print "Number of power traces:", T.shape[0]
    print "Number of poins each power trace:", M.shape[1]
    print "\n********************************************\n"
    Cor_matrix = all_pearson_matrices(T, M, 4)
    save(Cor_matrix, input_dir, "correlation_matrices")

    key_arr_dec = findKey(Cor_matrix)[::-1]
    key_arr_hex = map(to_hex, key_arr_dec)
    full_key_hex = "0x" + "".join(key_arr_hex)

    print "\n********************************************\n"
    print "Key Found:"
    print "Key bytes in HEX:", key_arr_hex
    print "Full key  in HEX:", full_key_hex
    print "Key bytes in DEC:", key_arr_dec
    print "\n********************************************\n"
