#!/usr/bin/env python

import random
import sys

if __name__ == "__main__":
    shuffled = random.sample(sys.argv[1:], len(sys.argv) - 1)
    print(" ".join(shuffled))
