# This script cleans call graphs 
# Example: Desktop\Work\tensorflow-master\tensorflow\python\framework\tensor_util._is_array_like -> tensor_util._is_array_like

#PLEASE MAKE A FOLDER WITH ANOTHER FOLDER INSIDE CALLED TEST - put your folder path in the variable below - uncomment the two variables below
# folder_path = r<your path here> + "\\"
# test_folder_path = r<your path here> + "\test\\"

import json
import os
import glob
import re
import pathlib
from pathlib import Path
import subprocess
path =  #<-THIS IS WHERE YOUR JSON FILES FROM PYCG ARE - FILL THIS IN 
listoffiles = glob.glob(path + "\*.json")
print(listoffiles)
pattern = re.compile(r'([^\\]+)\\([^\\]+)$')
i = 1
for json_graph in listoffiles:
    print(i)
    f = open(json_graph)
    try:
        old_dict = json.load(f)
    except json.decoder.JSONDecodeError:
        continue
    new_dict = {}
    for key in old_dict:
        new_key =""
        new_value_list = []
        #Check if the key contains tensorflow, if it does we want to filter it, change this

        if "tensorflow" in key: #<----------- change this to either TensorFlow or PyTorch

            #Assumption: the tensorflow keys have either \ or not, filter accordingly
            #Example: Desktop\Work\tensorflow-master\tensorflow\python\framework\tensor_util._is_array_like -> tensor_util._is_array_like
            if "\\" in key:
                #Use that regex filtering to perform it
                cleaned_key = pattern.search(key)
                part_1 = cleaned_key.group(1)
                part_2 = cleaned_key.group(2)
                new_key = part_1 + "." + part_2
                #Else split it with the dots and get the last 2 parts
                #Example: tensorflow.python.util.nest.flatten -> nest.flatten
            else:
                parts = key.split(".")
                new_key = ".".join(parts[-3:])

        else:
            new_key = key

        ## Do the same on the values
        for uncleaned_value in old_dict[key]:
            if "tensorflow" in uncleaned_value: #<----------- change this to either TensorFlow or PyTorch
                if "\\" in uncleaned_value:
                    cleaned_value = pattern.search(uncleaned_value)
                    part_1_value = cleaned_value.group(1)
                    part_2_value = cleaned_value.group(2)
                    new_value = part_1_value +"." + part_2_value
                else:
                    parts = uncleaned_value.split(".")
                    new_value = ".".join(parts[-3:])
                new_value_list.append(new_value)
            elif "tensorflow" not in uncleaned_value: #<----------- change this to either TensorFlow or PyTorch
                new_value_list.append(uncleaned_value)

        new_dict[new_key] = new_value_list
    i = i + 1

    # writing to file stuff
    # Change this
    current_filename_extension = os.path.basename(json_graph)
    current_filename = os.path.splitext(current_filename_extension)[0]
    if "test" in current_filename:
        filename = test_folder_path + current_filename + "_cleaned.json" #<----------- change this to either TensorFlow or PyTorch
        with open(filename, 'w') as fp:
            json.dump(new_dict, fp)

    else:
        filename = folder_path + current_filename + "_cleaned.json" #<----------- change this to either TensorFlow or PyTorch
        with open(filename, 'w') as fp:
            json.dump(new_dict, fp)





