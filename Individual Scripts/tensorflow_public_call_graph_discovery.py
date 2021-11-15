# This script discovers public functions in tensorflow annotated with tf.export

import ast
import os
import csv
import glob
import pandas as pd
import pathlib

tf_repo_path =  #<-- path of your tensorflow repo, fill this in
files = glob.glob(tf_repo_path + '/**/*.py', recursive=True)
public_function_destination = #Put a path where you want the public function

#ast parsing for tensorflow decorators
def flatten_attr(node):
    if isinstance(node, ast.Call):
        return str(flatten_attr(node.func)) + '.' + str(node.args)
    elif isinstance(node, ast.Name):
        return str(node.id)
    else:
        pass
     
publicfunctionlist = []

# Get a list of public functions with tf_export
for file in files:
    path = pathlib.PurePath(file)
    nameoffile = os.path.basename(file).replace('.py', '')
    foldername = os.path.basename(path.parent)
    parentfoldername = os.path.basename(path.parent.parent)
    print(file)

    try:
        with open(file) as f:
            tree = ast.parse(f.read(), filename=file)
    except UnicodeDecodeError:
        print("file failed")

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            found_decorators = []
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Name):
                    found_decorators.append(decorator.id)
                elif isinstance(decorator, ast.Call):
                        found_decorators.append(flatten_attr(decorator))
                
                    
            if "export" in '\t'.join(found_decorators):
                publicfunctionname = foldername +"." + nameoffile + "." + node.name
                publicfunctionlist.append(publicfunctionname)
              
with open(public_function_destination + "\\" + "tfpublicfunctions.csv", "w", newline='' ) as fp: #destination of your public function csv file
    wr = csv.writer(fp)
    for item in publicfunctionlist:
         wr.writerow([item])