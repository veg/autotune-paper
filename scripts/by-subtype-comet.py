import sys, os, csv
from collections import Counter

from Bio import SeqIO

subtypes = {}

base = sys.argv[1]

with open(os.path.join (base, "subtypes.csv")) as handle:
    reader = csv.reader (handle, delimiter = "\t")
    next (reader)
    for k in reader:
        try:
            support = float (k[3])
            tag = k[2]
            if tag not in subtypes:
                subtypes[tag] = []
            subtypes[tag].append (k[0])
        except:
            pass
            
     
id_mapper = {}
        
for k, v in subtypes.items():
    print (len (v))
    if len (v) >= 50:
        subtype_dir = os.path.join (base, k)
        try:  
            os.mkdir(subtype_dir)  
        except OSError as error:  
            pass
        subtype_writer = open (os.path.join (subtype_dir, "sequence.fasta"), "w")
        for id in v:
            id_mapper [id] = subtype_writer
                
with open(os.path.join (base, "sequence.msa")) as handle:
    for record in SeqIO.parse(handle, "fasta"):
        if record.id in id_mapper:
            print (">%s\n%s\n" % (record.id, record.seq), file = id_mapper[record.id])
     
