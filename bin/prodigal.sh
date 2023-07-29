#!/usr/bin/bash
#                       ----------------
#                       |   PRODIGAL   |
#                       ----------------
#Fast, reliable protein-coding gene prediction for prokaryotic genomes.

CONTIG=$1
EXT=$2 #contig extension
OUTDIR=$PWD/outfolder/str_annot
BASE=$(basename "$CONTIG" .${EXT})

mkdir -p $OUTDIR

prodigal -a $OUTDIR/${BASE}.aa.fa \
	 -d $OUTDIR/${BASE}.nuc.fa \
	 -i $CONTIG -f gff -p meta > $OUTDIR/${BASE}.gff

