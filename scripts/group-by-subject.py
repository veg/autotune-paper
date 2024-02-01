import sys, os
from collections import Counter

from Bio import SeqIO

by_subject = {}

base = sys.argv[1]

with open(os.path.join (base, "sequence.fasta")) as handle:
    for record in SeqIO.parse(handle, "fasta"):
        attributes = record.id.split ('.')
        if attributes[0] == 'B':
            pid = attributes[-1]
            if pid == '-':
                pid = record.id
            yr = attributes[2]
            if len (yr) > 1 and yr < '2013':
                if pid not in by_subject:
                    by_subject[pid] = (record, yr)
                else:
                    if yr < by_subject[pid][1]:
                        by_subject[pid] = (record, attributes[2])
                
     

for s,v in by_subject.items():
    print (">%s\n%s\n" % (v[0].id, v[0].seq))