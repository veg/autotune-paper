import sys, os
from collections import Counter

from Bio import SeqIO

subtypes = {}

base = sys.argv[1]

def get_tag (year):
    try:
        year = int (year)
        if year <= 2010:
            return "2010"
        if year <= 2016:
            return "2016"
        return "2024"
    except:
        return None

valid = set (["A","C","G","T"])

mean = 0
N = 0

with open(os.path.join (base, "unfiltered.fasta")) as handle:
    for record in SeqIO.parse(handle, "fasta"):
        r = len ([k for k in record.seq if k in valid]) / len (record.seq)
        mean += len (record.seq)
        if r > 0.95:
            print (">%s\n%s\n" % (record.id, record.seq))
        else:
            print (record.id, file = sys.stderr)
        N += 1
        
print ("Mean length = ", mean / N, file = sys.stderr)