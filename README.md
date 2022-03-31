# SCALP (SSR genotype calling pipeline)

## Input files

### Samples

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

### Primers
