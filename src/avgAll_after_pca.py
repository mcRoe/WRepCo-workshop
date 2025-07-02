#!/usr/bin/env python
'''
What to do: 
Take output from clusterPCA run and:
- rename -filename-_MOTL_Iter*.csv to -filename-_MOTL_Iter*.csv.bak
- rename pca-filename-_MOTL_Iter*.csv to -filename-_MOTL_Iter*.csv
- Run create class averages through averageAll

input rootName
check if filename == pca_filename without pca
'''

import argparse
import subprocess
#import pathlib
import os
import sys
import csv

def backup_original(filename_with_pca_prefix):
    ''' 
    Renames the basename_postfix to basename_postfix.bak
    '''
    orig = filename_with_pca_prefix.removeprefix("pca_")
    new = f"{orig}.bak"
    
    print(f"Renaming {orig} to {new}")
    os.rename(orig, new)   

def rename_pca(filename):
    pca_file = filename
    new = filename.removeprefix("pca_")
    
    print(f"Renaming {pca_file} to {new}")
    os.rename(pca_file, new)

def get_max_class_num(csvfile):
    class_max = 0
    with open(csvfile, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            class_number = int(row['class'])
        #    print(f'classno.: {class_number}')
            class_max = max(class_max, class_number)
    return class_max


def makePrm_avgAll(basename, class_no, iteration):
    # Copy the prm file and adding class number to the output filename
    orig_prm = f"{basename}.prm"
    class_prm = f"{basename}.prm.class{class_no}"


    if os.name == 'nt':  # Windows, just for testing (why not run in ubuntu?)
        cmd = f'copy "{orig_prm}" "{class_prm}"'
    else:  # Unix/Linux
        cmd = f'cp "{orig_prm}" "{class_prm}"'
        
    os.system(cmd)
    
    #Run averageALL with the iteration number from pca file
    
    with open (class_prm, 'a') as file:
        file.write(f'\nselectClassID = [{class_no}]')
    
    subprocess.run(f"averageAll {class_prm} {iteration}", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=True, shell=True)
    
    
    
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='')

    parser.add_argument('-b','--basename', type=str, required=True,
                        help='basename of project')
    parser.add_argument('-r','--revert', action='store_true',
                    help='renames .bak files to original. USE WITH CARE: OPERATION OVERWRITES PCA RESULTS')
    args = parser.parse_args()
    
    print(f"basename: {args.basename}\nrevert: {args.revert}")

    if args.revert:
        bak_fileNames = [filename for filename in os.listdir('.') if filename.endswith('.bak')]
        for filename in bak_fileNames:
            filename_noBak = filename.removesuffix('.bak')
            print(f'Renaming {filename} to {filename_noBak}')
            os.rename(filename, filename_noBak)

        sys.exit(0)

    max_class = 0
    pca_fileNames = [filename for filename in os.listdir('.') if filename.startswith(f'pca_{args.basename}_MOTL_Tom')]
    
    if not pca_fileNames:
        print("No pca files found")
        sys.exit(0)
    else:

        #Get iteration number from pca_...._Iter.csv file by extracting it from first item in list of pca_basename files
        filename_list = pca_fileNames[0].split('_')
        pca_iter = [iteration for iteration in filename_list if iteration.startswith('Iter')][0].removeprefix('Iter')
        
        #If MOTL list file ends with .csv, remove it. (Otherwise it will already be removed by split() operation)
        if pca_iter.endswith('.csv'):
            pca_iter = pca_iter.removesuffix('.csv')
        for x in pca_fileNames:
            max_class = max(max_class, get_max_class_num(x))
        
            print('-------  RENAMING FILES  -------')
            backup_original(x)
            rename_pca(x)
        
        
        print(f'------ GENERATING {max_class} CLASS AVERAGES FROM ITER {pca_iter} ------')


        for i in range(1,max_class+1):
            print(f'--- GENERATING CLASS AVERAGE {i} ---')
            makePrm_avgAll(args.basename, i, pca_iter)
