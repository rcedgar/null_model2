#!/usr/bin/python3

import sys
import numpy as np
from read_dist import read_dist

tsvfn = sys.argv[1]
edffn = "../edf/reseek_sensitive_ts.scop40.scop40." + sys.argv[2]

bin_mids, P_score_Fs = read_dist(edffn, "P_score_F")

def get_P_score_F(ts):
    return np.interp(ts, bin_mids, P_score_Fs)

f = open(tsvfn)
hdr = f.readline()
tss = []
P_pass_prefilters = []

tss = []
P_pass_prefilters = []
P_score_Fs2 = []

for line in f:
    flds = line.split('\t')
    assert len(flds) == 4
    ts = float(flds[0])
    P_pass_prefilter = float(flds[3])
    P_score_F = get_P_score_F(ts)

    tss.append(ts)
    P_pass_prefilters.append(P_pass_prefilter)
    P_score_Fs2.append(P_score_F)

nrbins = len(tss)

def get_cdf(binidx):
    cdf = 0
    for binidx2 in range(binidx, nrbins):
        cdf += P_pass_prefilters[binidx2]*P_score_Fs2[binidx2]
    return cdf

s = "newts"
s += "\tP_score_F"
s += "\tP_pass_prefilter"
s += "\tcdf"
print(s)

for binidx in range(nrbins):
    ts = tss[binidx]
    P_score_F = P_score_Fs2[binidx]
    P_pass_prefilter = P_pass_prefilters[binidx]

    cdf = get_cdf(binidx)

    s = "%.3g" % ts
    s += "\t%.3g" % P_score_F
    s += "\t%.3g" % P_pass_prefilter
    s += "\t%.3g" % cdf
    print(s)