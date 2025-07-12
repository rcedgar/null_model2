import sys
import random

calfn = sys.argv[1]
n = int(sys.argv[2])

random.seed(1)

label2lines = {}

for line in open(calfn):
	if line.startswith('>'):
		label = line
		label2lines[label] = []
	else:
		label2lines[label].append(line)

labels = list(label2lines.keys())
random.shuffle(labels)

for label in labels[:n]:
	sys.stdout.write(label)
	for line in label2lines[label]:
		sys.stdout.write(line)
