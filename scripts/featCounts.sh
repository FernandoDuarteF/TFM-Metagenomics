#!usr/bin/bash

GFF=$1
INS=$2
LIST=$(cat $INS)
BASEGFF=$(basename "$GFF" .gff)
OUTDIR=$PWD/outfolder/featCounts
OUTNAME=$OUTDIR/${BASEGFF}.tsv

mkdir -p $OUTDIR

featureCounts $LIST -p -a $GFF -o $OUTNAME -t CDS -g ID
