#!/usr/bin/python3

import sys
import argparse
import random
from skbio import Protein
from skbio.alignment import global_pairwise_align_protein, local_pairwise_align_protein
from skbio.sequence import SubstitutionMatrix
import fasta

AP = argparse.ArgumentParser()
AP.add_argument("--input", help="Input sequences (FASTA)")
AP.add_argument("--seed", type=int, required=True, help="Random number seed")
AP.add_argument("--reverse", help="Output reversed sequences (FASTA)")
AP.add_argument("--shuffle", help="Output shuffled sequences (FASTA)")
AP.add_argument("--db", help="Align input to this database (FASTA)")
AP.add_argument("--samples", type=int, default=10000, help="Nr. alignments to sample")
AP.add_argument("--test", default=False, action="store_true", help="Align hard-coded short test sequences")
AP.add_argument("--testq", default="GLFGAIAGFIKGG")
AP.add_argument("--testt", default="GLFDGLIAIGKGG")
AP.add_argument("--delete_segmask", default=False, action="store_true", help="Delete lower-case letters from this FASTA file")
AP.add_argument("--output", help="FASTA file")
AP.add_argument("--scores", help="Write scores to this file (text, one score per line)")
Args = AP.parse_args()

random.seed(Args.seed)

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

gap_open_penalty = 50
gap_extend_penalty = 5

if Args.test:
	seq1_str = Args.testq
	seq2_str = Args.testt

	# Convert the strings to scikit-bio Protein objects
	seq1 = Protein(seq1_str)
	seq2 = Protein(seq2_str)

	alignment_local, score_local, start_end_positions_local = \
			local_pairwise_align_protein(seq1, seq2, \
			substitution_matrix=mx, \
			gap_open_penalty = gap_open_penalty, \
			gap_extend_penalty = gap_extend_penalty)

	print(f"Sequence 1: {seq1_str}")
	print(f"Sequence 2: {seq2_str}")
	print(f"Aligned Sequence 1: {alignment_local[0]}")
	print(f"Aligned Sequence 2: {alignment_local[1]}")
	print(f"Alignment Score: {score_local}")
	sys.exit(0)

if Args.input is None:
	sys.stderr.write("--input or --test required\n")
	sys.exit(1)

seqs = fasta.ReadSeqsDict(Args.input)

labels = sorted(list(seqs.keys()))
sys.stderr.write("%d seqs\n" % len(labels))

if not Args.reverse is None:
	f = open(Args.reverse, "w")
	for label in labels:
		seq = seqs[label]
		fasta.WriteSeq(f, seq[::-1], label)
	f.close()
	sys.stderr.write(Args.reverse + " done.\n")
	sys.exit(0)

if not Args.shuffle is None:
	f = open(Args.shuffle, "w")
	for label in labels:
		seq = seqs[label]
		list_seq = list(seq)
		random.shuffle(list_seq)
		shuffled_seq = ''.join(list_seq)
		fasta.WriteSeq(f, shuffled_seq, label)
	f.close()
	sys.stderr.write(Args.shuffle + " done.\n")
	sys.exit(0)

if not Args.db is None:
	if Args.scores is None:
		sys.stderr.write("--scores required with --db\n")
	fscores = open(Args.scores, "w")
	db = fasta.ReadSeqsDict(Args.db)
	dblabels = list(db.keys())
	nrpairs = len(labels)*len(dblabels)
	nrfails = 0
	for sample in range(Args.samples):
		sys.stderr.write("%d %.4g%%\r" % (sample, (sample*100/Args.samples)))

		try:
			queryidx = random.randrange(0, len(labels)-1)
			dbidx = random.randrange(0, len(dblabels)-1)

			querylabel = labels[queryidx]
			dblabel = dblabels[dbidx]

			queryseq = seqs[querylabel]
			queryprotseq = Protein(queryseq)
			dbseq = db[dblabel]
			dbprotseq = Protein(dbseq)

			alignment_local, score_local, start_end_positions_local = \
					local_pairwise_align_protein(queryprotseq, dbprotseq, \
					substitution_matrix=mx, \
					gap_open_penalty = gap_open_penalty, \
					gap_extend_penalty = gap_extend_penalty)
		except:
			nrfails += 1
			continue
		fscores.write("%d\n" % score_local)

	fscores.close()
	sys.stderr.write("%s done, %d scores, %d fails\n" % (Args.scores, Args.samples, nrfails))
	sys.exit(0)

if Args.delete_segmask:
	nrseqsdeleted = 0
	if Args.output is None:
		sys.stderr.write("--output required with --delete_segmask\n")
		sys.exit(1)
	f = open(Args.output, "w")
	labels = sorted(list(seqs.keys()))
	for label in labels:
		seq = seqs[label]
		output_seq = ""
		for c in seq:
			if c.isupper():
				output_seq += c
		if len(output_seq) == 0:
			nrseqsdeleted += 1
			continue
		fasta.WriteSeq(f, output_seq, label)
		f.flush()
	sys.stderr.write("%s done, %d deleted\n" % (Args.output, nrseqsdeleted))
	f.close()