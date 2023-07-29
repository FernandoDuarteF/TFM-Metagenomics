#!/user/bin/bash

SEQ=$1
TYPE=$2
BASE=$(basename "$SEQ")
OUTDIR=$PWD/outfolder/clustering

mkdir -p $OUTDIR

cd-hit -i $SEQ -o $OUTDIR/$BASE -M 12000 -T 4

