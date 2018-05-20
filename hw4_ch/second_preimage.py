# Author: Hao CHENG
# Date: 17th April 2018

import hashlib
import argparse
import itertools


text = "It is a mathematical algorithm that maps data of arbitrary size to a bit string of a fixed size (a hash) and is designed to be a one-way function, that is, a function which is infeasible to invert."
text_chars = [chr(x) for x in range(14, 21)]
program_chars = ['\x09', '\x0A', '\x20', '#']
name = "HaoCHENG"


def hash_2_bytes(message):
    digest = hashlib.sha256(message.encode(encoding='utf_8')).hexdigest()[:4]
    return digest


def find_preimage(prefix, digest, suffix_size=8, chars=text_chars):
    possible_ascii = [chars for _ in range(suffix_size)]
    for n, suffix in enumerate(itertools.product(*possible_ascii)):
        if digest == hash_2_bytes(prefix + "".join(suffix)):
            return n, suffix
    else:
        return find_preimage(prefix, digest, suffix_size+1, chars)


def test_code_hash():
    with open(__file__, 'r+') as f:
        code = f.read()
        name_hash = hash_2_bytes(name)
        code_hash = hash_2_bytes(code)
        if code_hash != name_hash:
            print ("Finding preimage...")
            _, suffix = find_preimage(code, name_hash, chars=program_chars)
            f.seek(0)
            f.write(code + "".join(suffix))
            f.truncate()
            print ("Preimage of the code is found. Please run the program again.\n")
        else:
            print ("***Code hash:", code_hash)
            print ("***Name hash:", name_hash)


if __name__ == '__main__':
    test_code_hash()

    parser = argparse.ArgumentParser()
    parser.add_argument("d",  type=str)
    parser.add_argument("-p", "--prefix", type=str, default=text)

    args = parser.parse_args()

    print ("Prefix of the preimage:")
    print (text, "\n")
    print ("***Target hash value:", args.d.lower(), "\n")

    n, suffix = find_preimage(text, args.d.lower())
    print ("Suffix of the preimage is", suffix)
    print ("Preimage added with suffix:")
    print (text + "".join(suffix))
#
	#  #
