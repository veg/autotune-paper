### LANL full length genome sequence data

We queried the LANL HIV database (hiv.lanl.gov) on Jan 25th, 2024 by requesting full length genomes. The resulting records were filtered to include only a single sample per partient and exlcude problematic sequences. Remaining sequences were downloaded and split out by annotated subtype (as recorded in the database). Subtypes with ≥500 sequences were retained was subsequent analyses.

Each daughter subdirectory denotes the subtype and contains a `gene/sequence.fasta` file with aligned sequences for the corresponding gene.

The `gp41.fas` file was used as a reference passed to `bealign` for mapping.
