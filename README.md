# averageAll after pca classification in Imod's PEET 

This script takes output from clusterPCA run from Imod's PEET software and:
1. Renames **basename**_MOTL_Iter*.csv to **basename**_MOTL_Iter*.csv.bak
2. Renames pca_**basename**_MOTL_Iter*.csv to **basename**_MOTL_Iter*.csv
3. Run create class averages through averageAll


## Dependencies:

- Python

(Following packages are found on https://bio3d.colorado.edu/)  
- Imod 4.10 or greater
- PEET 13.0 or greater


## Options:

- -*b* or --*basename*  Similar to the fn name in the imod project
- -*r* or --*revert*    Reverts the .bak files to original. USE THIS FLAG WITH CARE: OPERATION WILL OVERWRITE PCA RESULTS

## Usage:
'avgAll_after.py -b 01_bin4_tomo01'
