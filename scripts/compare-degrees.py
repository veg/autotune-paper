import os, argparse, subprocess, re, sys, json, math, itertools, csv, shutil, random, itertools
from Bio import SeqIO

def    get_degrees (network):
    ids = network['Nodes']['id']
    degrees = {}
    for k in ids:
        degrees[k] = 0
    for k in ['source', 'target']:
        for n in network ['Edges'][k]:
            degrees[ids[n]] += 1
    return degrees

    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='compare network degree distros'
    )
    
    parser.add_argument(
        '-p', '--paper_json',
        type=str,
        help='the paper network JSON',
        required=True,
    )
    
    parser.add_argument(
        '-a', '--autotune_json',
        type=str,
        help='the autotune network JSON',
        required=True,
    )

   
    args = parser.parse_args()
    
    with open (args.paper_json, 'r') as fh:
        paper = json.load (fh)
        

    with open (args.autotune_json, 'r') as fh:
        autotune = json.load (fh)
    
    paper_d = get_degrees (paper)
    autotune_d = get_degrees (autotune)
    
    merged = set (paper_d.keys()).union (set (autotune_d.keys()))
    csv_writer = csv.writer (sys.stdout)
    csv_writer.writerow (['Node','Paper','Autotune'])
    for n in merged:
        csv_writer.writerow ([n,str (paper_d[n] if n in paper_d else 0), str (autotune_d[n] if n in autotune_d else 0)])
            
                
            
            
    
        
                
                            


