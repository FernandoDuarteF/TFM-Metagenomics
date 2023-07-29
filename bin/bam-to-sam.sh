#!/usr/bin/bash

BAM=$1
NAME=$(basename "$BAM" .bam)
OUTDIR=$PWD/outfolder/sam_files
mkdir -p $OUTDIR

samtools view -h $BAM > $OUTDIR/${NAME}.sam
