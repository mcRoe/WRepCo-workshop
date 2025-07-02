# Running the averageAll command with the outputs from a pca-classification

Dependencies:
Imod 4.10 or greater
PEET 13.0 or greater

This script takes output from clusterPCA run from Imod's PEET software and:
- renames **filename**_MOTL_Iter*.csv to **filename**_MOTL_Iter*.csv.bak
- rename pca_**filename**_MOTL_Iter*.csv to **filename**_MOTL_Iter*.csv
- Run create class averages through averageAll

Usage:
'avgAll_after '

Options:
