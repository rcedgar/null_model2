#!/usr/bin/python3

import sys
import math

mu = location = 0.152
beta = scale = 0.0242

for i in range(0, 10):
	TM = i/10
	ratio = (TM - mu)/beta
	p = 1 - math.exp(-math.exp(-ratio))
	s = "%.2f" % TM
	s += "  %.2e" % p
	print(s)