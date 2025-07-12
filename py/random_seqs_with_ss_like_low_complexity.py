#!/usr/bin/python3

import random
import argparse

AP = argparse.ArgumentParser()
AP.add_argument("--nrseqs", required=False, default=10000, help="Number of sequences to generate")
AP.add_argument("--minlen", required=False, type=int, default=100, help="Minimum seq length")
AP.add_argument("--maxlen", required=False, type=int, default=500, help="Maximum seq length")
AP.add_argument("--minrunlen", required=False, type=int, default=5, help="Minimum run length")
AP.add_argument("--maxrunlen", required=False, type=int, default=20, help="Maximum run length")
AP.add_argument("--mina", required=False, type=int, default=1, help="Minimum different letters per run")
AP.add_argument("--maxa", required=False, type=int, default=3, help="Maximum different letters per run")
AP.add_argument("--output", required=False, type=str, default="/dev/stdout", help="Output file (FASTA, default stdout)")

Args = AP.parse_args()
