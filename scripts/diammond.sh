#!/user/bin/bash

QUERY=$1
DB=$2
BASE=$(basename "$QUERY" .fastq.gz)
OUTDIR=$PWD/outfolder/counts

mkdir -p $OUTDIR

diamond blastx -d $DB -q $QUERY -v -p 12 -e 1e-5 --id 90 --query-cover 90 -a $OUTDIR/${BASE}.daa
