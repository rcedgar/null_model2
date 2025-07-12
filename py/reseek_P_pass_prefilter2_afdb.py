#!/usr/bin/python3

import sys
import numpy as np
from read_dist import read_dist

tsvfn = "afdb50.tsv"
edffn = "../edf/reseek_fast_ts.scop40.scop40." + sys.argv[1]

bin_mids, P_score_Fs = read_dist(edffn, "P_score_F")

'''
0       1       2       3
newts   N_all   N_fast  P
0.05    3514566 275     7.82e-05
0.1     1168598 1772    0.00152
0.15    236915  2027    0.00856
0.2     113112  2278    0.0201
0.25    63236   2355    0.0372
0.3     37427   2233    0.0597
0.35    24033   1862    0.0775
0.4     15729   1724    0.11
0.45    10088   1466    0.145
0.5     6896    1310    0.19
0.55    4634    1073    0.232
0.6     3016    925     0.307
0.65    1891    714     0.378
0.7     1187    573     0.483
0.75    689     403     0.585
0.8     454     307     0.676
0.85    302     232     0.768
0.9     191     153     0.801
0.95    125     98      0.784
1       95      74      0.779
1.05    63      57      0.905
'''

def get_P_score_F(ts):
    return np.interp(ts, bin_mids, P_score_Fs)

f = open(tsvfn)
hdr = f.readline()
# assert hdr.startswith("newts\tN_")
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
