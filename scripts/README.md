### Utility scripts

### `run-autotune.sh`

A simple task runner. Assumes that `bealign`, `tn93`, `bam2msa` and `hivnetworkcsv` are installed are included in the `PATH` variable.

Example run

```
$sh run-autotune.sh ../data/hiv-pol/Little-2014-24901437 HXB2_pol 0.015 0.05


Mean distance
0.0584193
AUTO-TUNE D = 0.02352, SCORE 1.5840499 98 40

AUTOTUNE THRESHOLD

832 edges on 380 nodes
Found 90 clusters
Maximum cluster size = 101 (second largest = 21) nodes
Unknown : 380
0 directed edges
{'Missing dates': 832}
Fitting the degree distribution to various densities
Best distribution is 'Waring' with rho = 3.00966 [2.69844 - 3.36733]

PUBLISHED THRESHOLD

460 edges on 303 nodes
Found 98 clusters
Maximum cluster size = 20 (second largest = 9) nodes
Unknown : 303
0 directed edges
{'Missing dates': 460}
Fitting the degree distribution to various densities
Best distribution is 'Waring' with rho = 3.69089 [3.20222 - 4.27465]


Running edge filtering on 33 clusters with 3 or more edges
4-cycle filtering a set of 276 edges (33/33 clusters). Pass 1, 5423 4-cycles, 0 filtered edges                                
Edge filtering identified 272 edges for removal
Edge filtering removed 272 edges
Fitting the degree distribution to various densities
Running edge filtering on 33 clusters with 3 or more edges
4-cycle filtering a set of 211 edges (33/33 clusters). Pass 2, 25 4-cycles, 0 filtered edgeses                                
Edge filtering identified 182 edges for removal
Edge filtering removed 182 edges
Fitting the degree distribution to various densities
1 {2, 3, 36, 34, 6, 38, 40, 43, 46, 47, 80, 87, 88, 89, 60, 62}
3 {26, 10}
4 {8, 83}
14 {24, 82}


```

Positional arguments

1. [REQ] Directory with a `sequence.fasta` file (results go in the same directory).
2. [REQ] Reference to pass as `-r` argument to `bealign` (one of the built-ins or a sequence file)
3. [REQ] The distance threshold used in the original publication (fraction)
4. [OPT] The maximum distance to consider for AUTO-TUNE calculations (fraction, default 0.05)
5. [OPT] Whether or not to overwrite intermediate files if they exist (0/1, default 0)
6. [OPT] Whether or not to perform edge filtering in network infernce (0/1, default 1)

Produces the follwing files

* `autotune.tsv` : the AUTOTUNE report by distance threshold
* `tn93.csv` : pairwise distances up to the maximum threshold
* `tn93.json` : TN93 report
* `sequence.bam`, `sequence.bam.bai`, `sequence.msa` : aligned sequences
* `network-autotune.json` : the transmission network at the AUTOTUNE thereshold
* `network-paper.json`:  the transmission network at the reference thereshold
* `network-constrast.json`:  the larger of the two networks (higher threshold) annoteted by the presence/absense in the smaller network and cluster numbers

### LANL partitioning strings

Python scripts to take a `.` delimited (LANL style) FASTA sequence headers (e.g. `A1D.SE.1994.SE7108.AF071473`), group them by the value of a particular field, and write the corresponding sequences to separate directories. They all take one positional argument which is a directory path (`DIR`), assumed to contain a `sequences.fasta` file. After the script is run, subdirectories (`DIR/X`) will be created (`X` is the value of the corresponding attribute), and these directories will contain `sequence.fasta` files

#### `by-subtype.py`

Split by subtype (minimum `100` sequences)

### `filter-N.py`

Remove sequences that have more than 5% of total length as non-resolved (not in `ACGT`) characters. Used to filter `clustuneR` based sequences. Takes one positional argument which is a directory path (`DIR`), assumed to contain an `unfiltered.fasta` file. Filtered sequences are written to `stdout`

### `group-by-subject.py`

Used to read LANL data and retain only one sequence per subject (earliest, if dates are known). Takes one positional argument which is a directory path (`DIR`), assumed to contain an `sequence.fasta` file. Filtered sequences are written to `stdout`. Used to filter `clustuneR` based sequences for the Seattle study (in `/data/clustunr/seattle/`)


### `inject-annotation.py`

A script to compare two networks built on the same data with different thresholds. Used internally by `run-autotune.sh`

### `by-subtype-comet.py` 

Similar to `by-subtype.py`, but uses subtypes from a `COMET` run (see `subtypes.csv` in data direcories). Takes one positional argument which is a directory path (`DIR`), assumed to contain an `sequence.fasta` file and a `subtypes.csv` file.
