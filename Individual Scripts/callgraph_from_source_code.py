#This script uses PYCG to get the call graphs of the files

import glob
import pathlib

import subprocess
import os
repo_path = # <--- THIS IS WHERE THE REPOSITORY YOU WANT TO SCAN IS (tensorflow/pytorch)
# Grabs all python files 
files = glob.glob(repo_path + '/**/*.py', recursive=True)
i = 1
callgraph_destination =   #THIS IS WHERE U WANT YOUR CALLGRAPHS TO END UP

for scanned_file_name in files:    
    print(scanned_file_name)
    jsonname = os.path.basename(scanned_file_name).replace('.py', '')
    path = pathlib.PurePath(scanned_file_name)
    foldername = os.path.basename(path.parent)
    parentfoldername = os.path.basename(path.parent.parent)
    jsonnewfile =  callgraph_destination +"\\" +str(foldername) +"_" + str(jsonname) +".json"
    print(jsonnewfile)
    with open(jsonnewfile, 'w') as outfile:
        subprocess.run(["pycg", scanned_file_name], stdout=outfile)

    i = i + 1


