import sys, os
from collections import Counter

from Bio import SeqIO

subtypes = {}

base = sys.argv[1]

with open(os.path.join (base, "sequence.fasta")) as handle:
    for record in SeqIO.parse(handle, "fasta"):
        tag = record.id.split ('.')[0]
        if tag not in subtypes:
            subtypes[tag] = []
        subtypes[tag].append (record.id)
     
id_mapper = {}
        
for k, v in subtypes.items():
    if len (v) >= 100:
        subtype_dir = os.path.join (base, k)
        try:  
            os.mkdir(subtype_dir)  
        except OSError as error:  
            pass
        subtype_writer = open (os.path.join (subtype_dir, "sequence.fasta"), "w")
        for id in v:
            id_mapper [id] = subtype_writer
                
with open(os.path.join (base, "sequence.fasta")) as handle:
    for record in SeqIO.parse(handle, "fasta"):
        if record.id in id_mapper:
            print (">%s\n%s\n" % (record.id, record.seq), file = id_mapper[record.id])
     
