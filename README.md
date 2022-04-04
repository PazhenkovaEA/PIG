# PIG (PIpeline for microsatellite Genotyping)

## Experiment design

Samples are grouped to **batches**, which correspond to 96-well (number of wells can vary) sample plates. Each position on plate (=each sample) is marked by unique combination of tags (short oligoes, connected to primers). It allows us to sequence multiple samples during one run. 
The pipeline is developed to analize data from multiplex PCR, when all loci of interest are proceeded in a single reaction. 
After sequencing, we need to demultiplex all the samples and loci and then to perform allele calling.
The main demultiplexing steps are based on OBITools3: https://git.metabarcoding.org/obitools/obitools3/blob/master/README.md

## Input files

### 1. Sequences

Illumina paired-end reads in .fastq format.

### 2. Samples

Tab-sepatated text file.

Example:

Position| Sample | Type
--- | --- | ---
A1|  bear1 | sample
A2|  blank1 | blank

**Sample**

Sample name. Please, avoid spaces, dots, backslashes  and special symbols in sample names.

**Postion**

Enumerated by capital letters (rows) and numbers (columns). Typically, 96-well plate contains 8 rows and 12 columns. Each position is marked by a pair of tags (see **Tags** section). 

**Type**:
  - sample
  - blank (empty well)
  - PCRNeg (no template in PCR)
  - ExtNeg (no sample in extraction)

### 3. Primers

Tab-sepatated text file.
Type: microsat or snp.
In case if the marker is biallelic or microsatellite contains different motifs, you need to provide all sequences or motifs with the same locus name.
Sequence (in the "sequence" column) should be provided without primers.

Example:

locus | primerF | primerR | type | motif |sequence
--- | --- | --- | --- | --- | ---
UA_03|  gctcccataac |gctcccataac | microsat | acac |
ZF|  cataacgctcc |taacgctcccataac | snp | | agag........tatac |


### 4. Tag combination file

Tab-sepatated text file.
If you have the only one primer plate, call the column PP1. 

**Important**. Make sure, that positions names in this file match to positions in the Sample description file. 

Example:

Position| PP1 | PP2
--- | --- | ---
A1|  acacacac:acacacac |caggctaa:tgagccta
B1|  acacacac:acagcaca |caggctaa:tgagcctt
..|  ...|...
H12|  gactgatg:gatcgcga |gaggacta:tcagtcga

### 5. Configuration file

Text file in .json format. 





