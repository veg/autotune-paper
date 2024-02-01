import os, argparse, subprocess, re, sys, json, math, itertools, csv, shutil, random, itertools
from Bio import SeqIO
import krippendorff

nodes = {}
edges = {}

def hivtrace_cluster_depthwise_traversal (nodes, edges):
  clusters = [[]]
  adjacency = {}
  by_node = {}

  
  for i,n in enumerate (nodes):
    n["visited"] = False
    n["cluster"] = None
    adjacency[i] = []

  for edge in edges:
    adjacency[edge["source"]].append (edge["target"])
    adjacency[edge["target"]].append (edge["source"])


  def traverse (nidx):
    node = nodes[nidx]
    if not node["id"] in by_node:
        clusters.append ([node])
        by_node[node["id"]] = len (clusters)
        node["cluster"]= by_node[node["id"]]
    node["visited"] = True
    
    for nid in adjacency[nidx]:
        neighbor = nodes[nid]
        if not neighbor["visited"]:
            by_node[neighbor["id"]] = by_node[node["id"]]
            neighbor["cluster"] = by_node[neighbor["id"]] 
            #print (by_node, clusters, file = sys.stderr)
            clusters[ by_node[neighbor["id"]] - 1].append (neighbor)
            traverse (nid)

    
  for i,n in enumerate (nodes):
      traverse (i)

  return clusters

def    unpack_array (D):
    if 'values' in D:
        res = []
        for d in D['values']:
            res.append (D['keys'][str(d)])
        return res
    return D
    
def     count_by (d):
    cnts = {}
    for i,v in d.items():
        if v not in cnts:
            cnts [v] = []
        cnts[v].append (i)
    return cnts
    
def    get_nodes_edges (network):
    ids = network['Nodes']['id']

    for nid in ids:
        if nid in nodes:
            nodes[nid] += 1
        else:
            nodes[nid] = 1
            
    src = unpack_array (network ['Edges']['source'])
    tgt = unpack_array (network ['Edges']['target'])
    
    for i,n in enumerate (src):
        n1 = ids[n]
        n2 = ids[tgt[i]]
        if n1 < n2:
            n1 = (n1, n2)
        else:
            n1 = (n2, n1)
            
        if n1 in edges:
            edges[n1] += 1
        else:
            edges[n1] = 1
            
    return ids

    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='compare network degree distros'
    )
    
    parser.add_argument(
        '-s', '--sequences',
        type=str,
        help='a file to read sequence IDs from',
        required=True,
    )

    
    parser.add_argument(
        '-n', '--networks',
        type=str,
        help='the paper network JSON',
        required=True,
        nargs = '*'
    )
    

   
    args = parser.parse_args()
    
    seqs = {}
    
    with open(args.sequences) as handle:
        for record in SeqIO.parse(handle, "fasta"):
            seqs [record.id] = set ()

    
    N_count = len (args.networks)
    
    for i, fp in enumerate (args.networks):
        with open (fp, 'r') as fh:
            for id in get_nodes_edges (json.load (fh)):
                seqs[id].add (i)
                
    reliability_data = [[] for k in range (N_count)]
   
    seqids  = list (seqs.keys ())
    for i in range (N_count):
        for si, seqid in enumerate (seqids):
            if i in seqs[seqid]:
                reliability_data[i].append (1)
            else:   
                reliability_data[i].append (0)
                
    print(krippendorff.alpha (reliability_data = reliability_data, level_of_measurement = "nominal"), file = sys.stderr)
    #print(','.join ([','.join ([str(i) for i in k]) for k in reliability_data]), file=sys.stderr)        
         
    joint_json = { 'Nodes' : [],
                   'Edges' : [],
                   'Settings' : {},
                   "patient_attribute_schema": {
                      "networks": {
                       "name": "networks",
                       "type": "String",
                       "label": "# of networks"
                      }
                     }
                  }
                   
    id_to_N = {}
    
    degrees = {}
     
    for n, ol in nodes.items():
        joint_json ['Nodes'].append (
            {
                'id' : n,
                'cluster' : 1,
                'degree' : 0,
                'patient_attributes' : {
                    'networks' : ol
                }
            }
        )
        id_to_N [n] = len (id_to_N)
        
    for e, ec in edges.items():
        joint_json ['Nodes'][id_to_N[e[0]]]['degree'] += 1
        joint_json ['Nodes'][id_to_N[e[1]]]['degree'] += 1
        joint_json["Edges"].append ({
            'source' : id_to_N[e[0]],
            'target' : id_to_N[e[1]],
            'length' : 0.1})
            
            
    degrees = [k['degree'] for k in joint_json['Nodes']]
    max_d = max (degrees)
    dd = [0 for k in range (max_d)]
    for k in degrees:
        dd[k-1] += 1
        
    joint_json['Degrees'] = {'Distribution' : dd}
    
    clusters = hivtrace_cluster_depthwise_traversal (joint_json["Nodes"],joint_json ["Edges"]) 
    
    complete_overlap = 0
    
    for c in clusters:
        if False not in [n["patient_attributes"]["networks"] == N_count for n in c]:
            complete_overlap +=1 
            
    print (complete_overlap, file = sys.stderr)
    
    joint_json['Cluster sizes'] = [len (k) for k in clusters]
         
    json.dump (joint_json, sys.stdout)
         
#    for k, nds in count_by (nodes).items():
#        print ("%d => %d" %  (k, len (nds))) 
#
#    for k, nds in count_by (edges).items():
#        print ("%d => %d" %  (k, len (nds))) 
    
        

   
            
                
            
            
    
        
                
                            


