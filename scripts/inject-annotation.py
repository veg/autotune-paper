import os, argparse, subprocess, re, sys, json, math, itertools, csv, shutil, random, itertools
from Bio import SeqIO

def    unpack_array (D):
    if 'values' in D:
        res = []
        for d in D['values']:
            res.append (D['keys'][str(d)])
        return res
    return D

def    make_value_dict (ids, vals):
    res = {}
    for i,d in enumerate (vals):
        res[ids[i]] = d
    return res
    
def    get_ids_from_fasta (path):
    ids = set ()
    with open (path, 'r') as fh:
        for record in SeqIO.parse(fh, "fasta"):
            ids.add (record.id)
    return ids
    
def    extract_edges (ids, src, target):
    edges = []
    for i, k in enumerate (src):
        if ids[k] < ids[target[i]]:
            edges.append ((ids[k], ids[target[i]]))
        else:
            edges.append ((ids[target[i]],ids[k]))
    return edges

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='compare network congruence'
    )
    
    parser.add_argument(
        '-r', '--reference_json',
        type=str,
        help='the reference network JSON',
        required=True,
    )
    
    parser.add_argument(
        '-c', '--compare_json',
        type=str,
        help='the comparator network JSON',
        required=True,
    )

    parser.add_argument(
        '-f', '--reference_fasta',
        type=str,
        help='the reference network FASTA',
        required=True,
    )
    
    parser.add_argument(
        '-t', '--compare_fasta',
        type=str,
        help='the comparator network FASTA',
        required=True,
    )
   
    args = parser.parse_args()
    
    srcAll = get_ids_from_fasta (args.reference_fasta)
    cmpAll = get_ids_from_fasta (args.compare_fasta)
    
    
    with open (args.reference_json, 'r') as fh:
        srcN = json.load (fh)
        
    srcN['patient_attribute_schema'] = {}
    srcN['patient_attribute_schema']['sampled'] = {"name" : "sampled", "label" : "Reference Network", "type" : "String"}
    srcN['patient_attribute_schema']['sampled_cluster'] = {"name" : "sampled_cluster", "label" : "Cluster in network at a different threshold", "type" : "String"}
    srcN['Nodes']['patient_attributes'] = {}
    
    srcClusters = make_value_dict(srcN['Nodes']['id'], unpack_array (srcN['Nodes']['cluster']))    
     
    srcByCluster = {}
    
    for k,c in srcClusters.items():
        if not c in srcByCluster:
            srcByCluster [c] = []
        srcByCluster [c].append (k)
        
    with open (args.compare_json, 'r') as fh:
        cmpN = json.load (fh)
 
    cmpClusters = make_value_dict(cmpN['Nodes']['id'], unpack_array (cmpN['Nodes']['cluster']))    
    
    id2idx = {}
    
    for i,n in enumerate (srcN['Nodes']['id']):
        srcN['Nodes']['patient_attributes'][i] = {}
        srcN['Nodes']['patient_attributes'][i]['sampled'] = 'Absent'
        srcN['Nodes']['patient_attributes'][i]['sampled_cluster'] = 'None'
        id2idx[n] = i
 
    for i,n in enumerate (cmpN['Nodes']['id']):
        srcN['Nodes']['patient_attributes'][id2idx[n]]['sampled'] = 'Present'
     
    T  = 0
    H  = 0   
    HE = 0
    coverage = []
    CN    = [0,0]
    
    for n in cmpAll:
        if n in srcClusters:
            CN[0] += 1
            if n in cmpClusters:
                CN[1] += 1
       
    for c,nodes in srcByCluster.items():
        sampled_cluster = [n for n in nodes if n in cmpAll]
        if len (sampled_cluster) >= 2: ## could have created at least a part of this cluster in the smaller network
            T += 1
            subsampled_clusters = set ()
            P = [0,0]
            #print (sampled_cluster, file = sys.stderr)
            for n1, n2 in itertools.combinations (sampled_cluster,2):
                   
                P[0] += 1
                if n1 in cmpClusters and n2 in cmpClusters and cmpClusters[n1] == cmpClusters[n2]:
                    srcN['Nodes']['patient_attributes'][id2idx[n1]]['sampled_cluster'] = str(cmpClusters[n1])
                    srcN['Nodes']['patient_attributes'][id2idx[n2]]['sampled_cluster'] = str(cmpClusters[n2])
                    subsampled_clusters.add (cmpClusters[n1])
                    P[1] += 1
                    
            if len (subsampled_clusters) > 1:
                print (c, subsampled_clusters, file = sys.stderr)
                H += 1
            if len (subsampled_clusters) == 1:
                HE += 1
            coverage.append (P[1] / float(P[0]))
            
            
json.dump (srcN, sys.stdout)            
            
                
            
            
    
        
                
                            


