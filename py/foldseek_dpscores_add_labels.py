import sys
import fasta

rcefn = "/mnt/c/src/foldseek_rce/out/rce_output.txt"
fafn = "../big_dbs/reseek/scop40_firstaa.fa"

seq2label = {}
def on_seq(label, seq):
	seq2label[seq] = label

fasta.ReadSeqsOnSeq(fafn, on_seq)

# C:\int\foldseek_rce2\src\strucclustutils\structurealign.cpp
	# if (1)
	# {//@@RCE
	# static std::mutex rce_lock;
	# rce_lock.lock();
	# static FILE *f = 0;
	# if (f == 0)
	#     {
	#     f = fopen("rce_output.txt", "w");
	#     //setbuf(f, 0);
	#     }
	# fprintf(f, "%.4g", align.evalue); // 1
	# fprintf(f, "\t%.4g", pvalue);     // 2
	# fprintf(f, "\t%d", fwdscore);     // 3
	# fprintf(f, "\t%d", diffscore);    // 4
	# fprintf(f, "\t%d", int(tSeqAA.getDbKey())); // 5
	# fprintf(f, "\t%d", querySeqLen);  // 6
	# fprintf(f, "\t%d", targetSeqLen); // 7
	# fprintf(f, "\t");
	# for (int i = 0; i < 12; ++i)      // 8
	#     {
	#     char c = qaa[i];
	#     if (c == 0)
	#         break;
	#     fprintf(f, "%c", c);
	#     }
	# fprintf(f, "\t");
	# for (int i = 0; i < 12; ++i)      // 9
	#     {
	#     char c = taa[i];
	#     if (c == 0)
	#         break;
	#     fprintf(f, "%c", c);
	#     }
	# fprintf(f, "\n");
	# rce_lock.unlock();
	# }//@@RCE


# evalue  
# 4e-73   -535.4  3016    2924    0       327     327     AYIAKQRQISFV    AYIAKQRQISFV
# 67      -1.343  45      4       0       78      327     FQTWEEFSRAAE    AYIAKQRQISFV

linenr = 0
badlines = 0
missing = 0
mindiffscore = 0
for line in open(rcefn):
	linenr += 1
	flds = line[:-1].split('\t')
	if len(flds) != 9:
		badlines += 1
		continue
	fwdscore = int(flds[2])
	diffscore = int(flds[3])
	qseq = flds[7]
	tseq = flds[8]
	qlabel = seq2label.get(qseq)
	tlabel = seq2label.get(tseq)
	if qlabel is None or tlabel is None:
		missing += 1
		continue
	s = qlabel
	s += "\t" + tlabel
	s += "\t%d" % fwdscore
	s += "\t%d" % diffscore
	if diffscore < mindiffscore:
		mindiffscore = mindiffscore
	print(s)

pct = badlines*100/linenr
pctmissing = missing*100/linenr
sys.stderr.write("%d / %d bad lines (%.3g%%)\n" % (badlines, linenr, pct))
sys.stderr.write("%d / %d missing (%.3g%%)\n" % (missing, linenr, pctmissing))
sys.stderr.write("min diffscore = %d\n" % mindiffscore)
