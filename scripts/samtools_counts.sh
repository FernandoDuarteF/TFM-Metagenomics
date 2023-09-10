#!usr/bin/bash

BAM=$1
ID=$(basename "$BAM" .bam)
OUTDIR=$PWD/outfolder/counts_bam
TEMPT=$PWD/tmp

mkdir -p $OUTDIR && mkdir -p $TEMPT

echo "${ID}..."

samtools view -f 67 -b $BAM > $TEMPT/${ID}.bam

echo "'samtools view -f 67 -b ${BAM} > ${TEMPT}/${ID}.bam' finished"

samtools index $TEMPT/${ID}.bam

samtools idxstats $TEMPT/${ID}.bam | cut -f1,3 | grep -v "\*" | awk '$2!=0 {print $0}' > $OUTDIR/${ID}

echo "'samtools idxstats ${TEMPT}/${ID}.bam | cut -f1,3 | grep -v "\*" | awk '$2!=0 {print $0}' > ${OUTDIR}/${ID}' finished"

rm -r $TEMPT

echo "${TEMPT} removed"
