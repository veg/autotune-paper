### LANL sequence data

We queried the LANL HIV database (hiv.lanl.gov) on Jan 25th, 2024 by using `2253-3200` in the `start` and `end` search fields. The resulting records were filtered to include only a single sample per partient and exlcude problematic sequences. Remaining sequences were downloaded and split out by annotated subtype (as recorded in the database). Subtypes with ≥1000 sequences were retained was subsequent analyses.

Each daughter subdirectory denotes the subtype and contains a `sequence.fasta` file with unaligned sequences.
