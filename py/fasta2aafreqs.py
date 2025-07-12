import sys
import fasta

def OnRec(Label, Seq):
	global Counts
	for c in Seq:
		 i = ord(c.upper())
		 Counts[i] += 1

Counts = []
for i in range(0, 256):
	Counts.append(0)

fasta.ReadSeqsOnSeq(sys.argv[1], OnRec)

AminoChars = "ACDEFGHIKLMNPQRSTVWY"

N = 0
for c in AminoChars:
	N += Counts[ord(c)]

print("letter2freq = {}")
Sum = 0
for c in AminoChars:
	i = ord(c)
	f = float(Counts[i])/N
	Sum += f
	print("letter2freq['%c'] = %.6g" % (c, f))
print("# sum = %.5f" % Sum)
