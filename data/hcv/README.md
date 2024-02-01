### HCV sequence data

Each directory contains all (unaligned) HCV sequences as a `FASTA` file associated with a particular paper as `sequence.fasta`. Typically those were retrieved by using GenBank accession numbers in each paper. We also examined GenBank PopSets associated with the sequences because sometimes those contained more submitted data that given by the published accesstion numbers.

Several directories also contain `subtype.csv` files which are inferred viral subtypes (using the online COMET service at https://comet.lih.lu).

For those directories, there are also subdirectories with sequences split out by subtype.

The name of the directory is formatted as `FirstAuthorLastName-Year-PUBMED ID`

The `reference` directories contain reference sequences supplied to `bealign` for mapping.