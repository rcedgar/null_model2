#!/usr/bin/python3

import fasta

label1 = "d2il5a1"
label2 = "d2xsta_"

# 3Di substitution matrix
# Reverse-engineered from Foldseek source code
mx = {}
mx['A'] = { 'A': 24, 'C':-12, 'D':  4, 'E':  8, 'F': 12, 'G': -8, 'H': -8, 'I':-29, 'K':-12, 'L':-12, 'M':-41, 'N':-20, 'P': -4, 'Q':  4, 'R':-16, 'S':-29, 'T':-20, 'V':-25, 'W':  0, 'Y': -8 }
mx['C'] = { 'A':-12, 'C': 24, 'D': -8, 'E':-33, 'F':-20, 'G':-16, 'H':-16, 'I':-49, 'K':-53, 'L':  4, 'M':-57, 'N':  0, 'P':  0, 'Q':  4, 'R': -4, 'S':  0, 'T':-33, 'V':  4, 'W':-29, 'Y':-37 }
mx['D'] = { 'A':  4, 'C': -8, 'D': 16, 'E':-12, 'F':  0, 'G':  4, 'H':  4, 'I':-12, 'K':-20, 'L':-16, 'M':-20, 'N': -8, 'P':  4, 'Q': -4, 'R': -4, 'S':-16, 'T': -8, 'V':-12, 'W': -8, 'Y': -8 }
mx['E'] = { 'A':  8, 'C':-33, 'D':-12, 'E': 36, 'F': -8, 'G':-29, 'H':-16, 'I':-49, 'K':-41, 'L':-29, 'M':-69, 'N':-33, 'P':-25, 'Q':-12, 'R':-33, 'S':-41, 'T':-41, 'V':-53, 'W':-25, 'Y':-12 }
mx['F'] = { 'A': 12, 'C':-20, 'D':  0, 'E': -8, 'F': 28, 'G':-12, 'H':-12, 'I':-20, 'K':  4, 'L':-12, 'M':-37, 'N':-20, 'P': -8, 'Q':  8, 'R':-20, 'S':-33, 'T':-12, 'V':-29, 'W': 16, 'Y':-16 }
mx['G'] = { 'A': -8, 'C':-16, 'D':  4, 'E':-29, 'F':-12, 'G': 24, 'H': 12, 'I':  0, 'K':-29, 'L':-29, 'M': -4, 'N': -8, 'P': -8, 'Q':-16, 'R': 12, 'S':-12, 'T': 16, 'V':-25, 'W':-16, 'Y': -8 }
mx['H'] = { 'A': -8, 'C':-16, 'D':  4, 'E':-16, 'F':-12, 'G': 12, 'H': 24, 'I':-16, 'K':-29, 'L':-25, 'M':-25, 'N':  0, 'P': -4, 'Q':-12, 'R':  4, 'S':-12, 'T': -4, 'V':-20, 'W':-20, 'Y': 12 }
mx['I'] = { 'A':-29, 'C':-49, 'D':-12, 'E':-49, 'F':-20, 'G':  0, 'H':-16, 'I': 32, 'K':-20, 'L':-45, 'M': 28, 'N':-29, 'P':-25, 'Q':-25, 'R':-12, 'S':-37, 'T': 24, 'V':-49, 'W':-20, 'Y':-33 }
mx['K'] = { 'A':-12, 'C':-53, 'D':-20, 'E':-41, 'F':  4, 'G':-29, 'H':-29, 'I':-20, 'K': 36, 'L':-45, 'M':-33, 'N':-49, 'P':-25, 'Q':-20, 'R':-37, 'S':-57, 'T':-20, 'V':-61, 'W': 20, 'Y':-33 }
mx['L'] = { 'A':-12, 'C':  4, 'D':-16, 'E':-29, 'F':-12, 'G':-29, 'H':-25, 'I':-45, 'K':-45, 'L': 24, 'M':-65, 'N':-12, 'P': -8, 'Q':  8, 'R':-16, 'S':-16, 'T':-37, 'V':  0, 'W':-33, 'Y':-37 }
mx['M'] = { 'A':-41, 'C':-57, 'D':-20, 'E':-69, 'F':-37, 'G': -4, 'H':-25, 'I': 28, 'K':-33, 'L':-65, 'M': 40, 'N':-37, 'P':-37, 'Q':-41, 'R':-20, 'S':-41, 'T': 12, 'V':-65, 'W':-25, 'Y':-37 }
mx['N'] = { 'A':-20, 'C':  0, 'D': -8, 'E':-33, 'F':-20, 'G': -8, 'H':  0, 'I':-29, 'K':-49, 'L':-12, 'M':-37, 'N': 28, 'P':  0, 'Q': -8, 'R':  8, 'S': 12, 'T':-16, 'V':  0, 'W':-33, 'Y':-20 }
mx['P'] = { 'A': -4, 'C':  0, 'D':  4, 'E':-25, 'F': -8, 'G': -8, 'H': -4, 'I':-25, 'K':-25, 'L': -8, 'M':-37, 'N':  0, 'P': 16, 'Q':  0, 'R':  0, 'S': -8, 'T':-16, 'V':  0, 'W':-16, 'Y':-20 }
mx['Q'] = { 'A':  4, 'C':  4, 'D': -4, 'E':-12, 'F':  8, 'G':-16, 'H':-12, 'I':-25, 'K':-20, 'L':  8, 'M':-41, 'N': -8, 'P':  0, 'Q': 20, 'R': -8, 'S':-16, 'T':-20, 'V': -4, 'W': -8, 'Y':-20 }
mx['R'] = { 'A':-16, 'C': -4, 'D': -4, 'E':-33, 'F':-20, 'G': 12, 'H':  4, 'I':-12, 'K':-37, 'L':-16, 'M':-20, 'N':  8, 'P':  0, 'Q': -8, 'R': 24, 'S':  8, 'T':  0, 'V': -4, 'W':-25, 'Y':-12 }
mx['S'] = { 'A':-29, 'C':  0, 'D':-16, 'E':-41, 'F':-33, 'G':-12, 'H':-12, 'I':-37, 'K':-57, 'L':-16, 'M':-41, 'N': 12, 'P': -8, 'Q':-16, 'R':  8, 'S': 24, 'T':-25, 'V':  0, 'W':-45, 'Y':-37 }
mx['T'] = { 'A':-20, 'C':-33, 'D': -8, 'E':-41, 'F':-12, 'G': 16, 'H': -4, 'I': 24, 'K':-20, 'L':-37, 'M': 12, 'N':-16, 'P':-16, 'Q':-20, 'R':  0, 'S':-25, 'T': 32, 'V':-37, 'W':-20, 'Y':-20 }
mx['V'] = { 'A':-25, 'C':  4, 'D':-12, 'E':-53, 'F':-29, 'G':-25, 'H':-20, 'I':-49, 'K':-61, 'L':  0, 'M':-65, 'N':  0, 'P':  0, 'Q': -4, 'R': -4, 'S':  0, 'T':-37, 'V': 12, 'W':-41, 'Y':-45 }
mx['W'] = { 'A':  0, 'C':-29, 'D': -8, 'E':-25, 'F': 16, 'G':-16, 'H':-20, 'I':-20, 'K': 20, 'L':-33, 'M':-25, 'N':-33, 'P':-16, 'Q': -8, 'R':-25, 'S':-45, 'T':-20, 'V':-41, 'W': 32, 'Y':-25 }
mx['Y'] = { 'A': -8, 'C':-37, 'D': -8, 'E':-12, 'F':-16, 'G': -8, 'H': 12, 'I':-33, 'K':-33, 'L':-37, 'M':-37, 'N':-20, 'P':-20, 'Q':-20, 'R':-12, 'S':-37, 'T':-20, 'V':-45, 'W':-25, 'Y': 36 }

def get_seq(label, ext):
	seqs = fasta.ReadSeqsDict(label + '.' + ext)
	labels = list(seqs.keys())
	return seqs[labels[0]]

ss1 = get_seq(label1, "ss")
ss2 = get_seq(label2, "ss")

aa1 = get_seq(label1, "aa")
aa2 = get_seq(label2, "aa")

tdi1 = get_seq(label1, "3di")
tdi2 = get_seq(label2, "3di")

tdi1u = tdi1.upper()
tdi2u = tdi2.upper()

L1 = len(ss1)
assert len(aa1) == L1
assert len(tdi1) == L1

L2 = len(ss2)
assert len(aa2) == L2
assert len(tdi2) == L2

n1 = 0
for c in tdi1:
	if c.islower():
		n1 += 1

n2 = 0
for c in tdi2:
	if c.islower():
		n2 += 1

row1 = None
row2 = None
n = 0
def OnSeq(label, seq):
	global n
	global row1, row2
	if n == 0:
		row1 = seq
	elif n == 1:
		row2 = seq
	else:
		assert False
	n += 1
fasta.ReadSeqsOnSeq("pair.3di.aln", OnSeq)

seg1 = row1.replace('-', '').upper()
seg2 = row2.replace('-', '').upper()

pos1 = tdi1u.find(seg1)
pos2 = tdi2u.find(seg2)

nrcols = len(row1)
assert len(row2) == nrcols

ssrow1 = ""
ssrow2 = ""

aarow1 = ""
aarow2 = ""
maskedrow1 = ""
maskedrow2 = ""
localpos1 = pos1
localpos2 = pos2
annot = ""
idents = 0
positives = 0
for col in range(nrcols):
	c1 = row1[col]
	c2 = row2[col]
	if c1 == '-' or c2 == '-':
		annot += ' '
	elif c1 == c2:
		annot += '|'
		idents += 1
		positives += 1
	elif mx[c1][c2] > 0:
		positives += 1
		annot += '+'
	else:
		annot += ' '

	if c1 == '-':
		ssrow1 += '-'
		maskedrow1 += '-'
		aarow1 += '-'
	else:
		aarow1 += aa1[localpos2]
		maskedrow1 += tdi1[localpos1]
		ssrow1 += ss1[localpos1]
		localpos1 += 1

	if c2 == '-':
		ssrow2 += '-'
		maskedrow2 += '-'
		aarow2 += '-'
	else:
		aarow2 += aa2[localpos2]
		maskedrow2 += tdi2[localpos2]
		ssrow2 += ss2[localpos2]
		localpos2 += 1

print(ssrow1[0:60])
print(aarow1[0:60])
print(maskedrow1[0:60] + "  " + label1)
print(annot[0:60])
print(maskedrow2[0:60] + "  " + label2)
print(aarow2[0:60])
print(ssrow2[0:60])
print(ssrow1[0:60])

print()
print()
print(aarow1[60:])
print(maskedrow1[60:] + "  " + label1)
print(annot[60:])
print(maskedrow2[60:] + "  " + label2)
print(aarow2[60:])
print(ssrow2[60:])

s = "Score 992, Identities %d/%d (%.1f%%)" % (idents, nrcols, idents*100/nrcols)
s += ", Positives %d/%d (%.1f%%)" % (positives, nrcols, positives*100/nrcols)
print(s)

print("Segmasked %s %d/%d (%.1f%%)" % (label1, n1, L1, n1*100/L1))
print("Segmasked %s %d/%d (%.1f%%)" % (label2, n2, L2, n2*100/L2))