### 01/07/2023

Sequences were assembled using megahit into a single assembly. This was done to make the task of differential abundance genes easier, since we only have one assembly for gene prediction, this way we will have ofrs than can be compared between samples. View paper, since apparently this is recommended for cross sample comparision, but is also important to consider the possible bias of this methos between samples of very different origin (for example, microbiome samples between different idividuals).

Dowloaded bam alignments from galaxy using:

```
wget https://usegalaxy.org/api/histories/e881e1169bd9c300/contents/dataset_collections/bb29577376c9153b/download?key=86952da515bf0b02f43d53a508d408f8
```
, and then uncompressed the file renaming it so that in includes the zip extension using:

```
mv 'download?key=86952da515bf0b02f43d53a508d408f8.1' bams.zip
gunzip bams.zip
mv 'Map with BWA-MEM on collection 7 (mapped reads in BAM format)'/* .
```

### 02/07/2023

Added TFM variable to ```.bashrc```. Invoke using ```$TFM```.

```*.bam``` files from ```bam_files``` were intended to be converted to ```sam``` files, but sam files are heavier and more difficult to handle in terms of computational power, since ```bam``` files are no readable binary files, and therefore enough for the tasks being carried out (view https://gatk.broadinstitute.org/hc/en-us/articles/360035890791-SAM-or-BAM-or-CRAM-Mapped-sequence-data-formats). Either way, it was run using the following commnad (before process was killed):

```
for i in bam_files/*.bam; do bash bin/bam-to-sam.sh $i & done > log &
```

Prodigal run on ```*.bam``` files from ```bam_files``` folder using:

```
bash bin/prodigal.sh assemblies/co-assembly.fasta fasta & > prodigal_log &
```

Looks like the & here is useless.

### 03/07/2023

Packages featurecounts and htseq were installed in counts conda environment. Both were tested. First featurecounts using this in the command line

Do ```echo path/*.bam``` for ```bams``` list

FeatureCounts was run using the following commnad:

```
bash bin/featCounts.sh outfolder/str_annot/co-assembly.gff bam_list
```

```-g ID```, ```-t CDS``` and ```-p``` must be specified

```
failed to find the gene identifier attribute in the 9th column of the provided GTF file.
The specified gene identifier attribute is 'gene_id'
```

Feature counts was run successfully after the parameters have been specified.

### 04/07/2023

Afeter doing the clustering with CD-HIT using ```bash bin/cdhit.sh outfolder/str_annot/co-assembly.aa.fa &> cdhit.glo &```, I noticed that I would have a problem with gene abundances, since featureCounts uses non redundant gff file from prodigal. Therefore I cannot use this counts. I need to assmebly to the ARG catalogue using BWA or the clustered sequences from CD-HIT. Do this using BWA for every sample.

Might need to map the reads to de ARG database and extract the counts from there


diamond makedb --in protein_fasta_protein_homolog_model.fasta -d card-database

Increased ram using C/Users/dfern/.wslconfig

In order to

ln -s /mnt/e/Users/dfern/TFM/secuencias sequences

### 16/07/2023

Since sequences needed to be decompressed for metaxa to run, sequencec files were dived betweem ```first_half``` and ```second_half``` folders. Metaxa was run using:

```
for i in sequences/first_half/*_1.fastq.gz; do bash bin/metaxa2.sh $i; done
```

```
for i in sequences/second_half/*_1.fastq.gz; do bash bin/metaxa2.sh $i; done
```

This will give us the number of 16S bacteria sequences per library. We can use this number to normalize the counts and getting rid of composition bias, instead of using the library depth which do not account for this (@lalguptaPlatformsElucidatingAntibiotic2020).

Be clear that approach has been changed, for now two options are being considered for retrieving ARGs: BWA and Diamond to map the reads to the ARGs protein catalogue from CARD.

### 24/07/2023

It is good practice to always count the number of reads for each file. You cand do this using this script:

### 25/07/2023

Downloaded ```fastq.gz``` from galaxy collection again, size of the compressed file is 48.89G

Rename files using:

```
# for forward reads
for i in */reverse.*.gz; do id=$(echo $i | cut -d"/" -f1); mv $i ${id}_1.fastq.gz; done
# for reverse reads
for i in */forward.*.gz; do id=$(echo $i | cut -d"/" -f1); mv $i ${id}_2.fastq.gz; done
```