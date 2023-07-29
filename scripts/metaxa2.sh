#!/user/bin/bash

F=$1
R=${F%_1.fastq.gz}_2.fastq.gz
BASE=$(basename "$F" _1.fastq.gz)
OUTDIR=$PWD/outfolder/metaxa

echo $BASE

F_d=${F%.gz}
R_d=${R%.gz}

mkdir -p $OUTDIR

pigz -d -k -p12 $F #-k is to keep original file
pigz -d -k -p12 $R

metaxa2 -1 $F_d -2 $R_d -o $OUTDIR/$BASE --mode m -t bacteria --cpu 12

rm $F_d #change for pigz -p12 $F_d if necesary
rm $R_d #change for pigz -p12 $R_d if necesary
