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

### 29/07/2023

It's good practice to check the number of reads in each sample. This can be done using the next command:

```
for i in *.fastq.gz; do echo $i; echo $(zcat $i | wc -l)/4 | bc; done > number-reads
```

``pandoc README.md -o README.pdf --bibliography=README.bib``

### 31/07/2023

To get the counts from the bam file with the reads mapped to the protein catalog, we first need to get rid of the unmapped reads:

```
samtools view -b -F 4 file.bam > mapped.bam
```

After this, we need to create an index for the new bam file:

```
samtools index mapped.bam
```

Once we have the index, we can use samtool's idxstats to get the read mapped to each protein;

```
samtools idxstats mapped.bam
```

Here the first column would be the reference id, the second column the mapped reads, and the third the unmapped reads. Unmapped reads means that although one of reads was mapped, the other pair remained unmapped.

### 01/07/2023

Once reads have bee mapped to the calogue, the next step before filtering should be to check the alignment stats;

```
samtools flagstat file.bam
```

Look for mapped reads and properly mapped reads. For the counts, seems logical to choose one of the pairs that has a properly mapped pair. *IMPORTAT: AM I LOOSING INFORMATION WITH THIS APPROACH (SELECTING ONLY PROPERLY MAPPED READS)* Might be necesssary to check.

To extract the read counts for every protein did the following:

```
# First select one of the pair whoose mate is properly mapped
samtools view -f 67 -b file.bam > mapped_pair.bam
# Check again
samtools flagstat mapped_pair.bam
# Create index 
samtools index mapped_pair.bam
# Use indxstats to extract the counts and create counts files
samtools idxstats mapped_pair.bam | cut -f1,3 | grep -v "\*" | awk '$2!=0 {print $0}' > counts.txt
```

``cut`` is used here retrieve the id column and the mapped reads counts column. Use this broad institute https://broadinstitute.github.io/picard/explain-flags.html page to check for the different flags to extract reads properly with ``samtools view``. awk is used to remve those proteins with 0 counts.

### 07/08/2023

It is advisable to also remove duplicates from the bam files, therefore ``-F 1024`` flag needs to be added:


Also, to remove reads of a pair that map to different genes using mapping quality, instead of mapped in proper pairs, for filtering might be an option.