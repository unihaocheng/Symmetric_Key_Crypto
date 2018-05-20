# Author: Hao CHENG
# Date: 17th April 2018

import hashlib, random, time, os
from string import digits, ascii_uppercase, ascii_lowercase
from itertools import product

chars = digits + ascii_uppercase + ascii_lowercase


def getHash(message, k, prefix):
  return hashlib.sha256(prefix + message).hexdigest()[:k]


def brent(k, prefix, initial):

  x0 = initial
  m0 = None
  m1 = None

  power  = lam = 1
  tortoise = x0
  hare   = getHash(tortoise, k, prefix)       # f(x0)

  # Search for a match
  while tortoise != hare:
    if power == lam:                          # Checks to see if it needs a new power of 2
      tortoise = hare
      power *= 2
      lam = 0
    hare = getHash(hare, k, prefix)
    lam += 1                                  # length+1

  # At this point, same hash is found
  # Find Position of the first repetition
  mu = 0                                      # Index of the first element of the cycle
  tortoise = hare = x0                        # Set back to initial
  for i in range(lam):
    # "range(lam) produces list with values 0, 1, ..., lam-1"
    hare = getHash(hare, k, prefix)           # distance b/w tortoise and hare is now lambda

  # Hare and tortoise move at same speed until they agree
  while tortoise != hare:
    m0 = tortoise
    m1 = hare
    tortoise = getHash(tortoise, k, prefix)   # f(tortoise)
    hare   = getHash(hare, k, prefix)         # f(hare)
    mu += 1                                   # Looking from the point of first repetition

  if mu is 0:
    print "Failed to find a collision: x0 was in a cycle!"
    return

  print_results(m0, m1, getHash(m0, k, prefix), k, prefix)


def print_results(m0, m1, hash, k, prefix):
  print "===== Collision Found! ====="
  print "Message A:  ", prefix + m0
  print "Full Hash:  ", hashlib.sha256(prefix + m0).hexdigest()
  print "Message B:  ", prefix + m1
  print "Full Hash:  ", hashlib.sha256(prefix + m1).hexdigest()
  print "k Collision:", hash
  print "k Size:     ", k
  print "Time taken: ", time.time() - start_time
  print "\n"
  print ('\a')

if __name__ == '__main__':
    # Keep track of how long it takes to find a k collision
    start_time = time.time()
    print "Script started at:", start_time
    print "\n"
    brent(14, "HaoCHENG", "1")
