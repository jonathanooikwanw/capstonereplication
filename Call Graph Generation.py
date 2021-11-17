# This script cleans call graphs 
# Example: Desktop\Work\tensorflow-master\tensorflow\python\framework\tensor_util._is_array_like -> tensor_util._is_array_like

import json
import os
import glob
import re
import pathlib
from pathlib import Path
import subprocess

directory_of_script = os.path.dirname(__file__)  # directory of script
uncleaned_call_graph_folder = r'{}\graphs'.format(directory_of_script)  # path to be created

try:
    os.makedirs(uncleaned_call_graph_folder)
except OSError:
    pass


def pyCG():
    # Path to your repository
    path = #<--- CHANGE THIS TO YOUR TENSORFLOW OR PYTORCH REPOSITORY
    files = glob.glob(path + '/**/*.py', recursive=True)

    for scanned_file_name in files:
        jsonname = os.path.basename(scanned_file_name).replace('.py', '')
        path = pathlib.PurePath(scanned_file_name)
        foldername = os.path.basename(path.parent)
        parentfoldername = os.path.basename(path.parent.parent)
        jsonpath = uncleaned_call_graph_folder + "\\" + str(parentfoldername) + "_" + str(foldername) + "_" + str(jsonname) + ".json"
        with open(jsonpath, 'w') as outfile:
            subprocess.run(["pycg", scanned_file_name], stdout=outfile)



def cleaning():
    listoffiles = glob.glob(uncleaned_call_graph_folder + "\*.json")
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
            new_key = ""
            new_value_list = []
            # Check if the key contains tensorflow, if it does we want to filter it, change this
            
            if "tensorflow" in key:  # <--------- Change this to either "tensorflow" or "pytorch:
                
                # Assumption: the tensorflow keys have either \ or not, filter accordingly
                # Example: Desktop\Work\tensorflow-master\tensorflow\python\framework\tensor_util._is_array_like -> tensor_util._is_array_like
                if "\\" in key:
                    # Use that regex filtering to perform it
                    cleaned_key = pattern.search(key)
                    print(cleaned_key)
                    part_1 = cleaned_key.group(1)
                    part_2 = cleaned_key.group(2)
                    new_key = part_1 + "." + part_2
                    # Else split it with the dots and get the last 2 parts
                    # Example: tensorflow.python.util.nest.flatten -> nest.flatten
                else:
                    parts = key.split(".")
                    new_key = ".".join(parts[-3:])

            else:
                new_key = key

                ## Do the same on the values
            for uncleaned_value in old_dict[key]:
                # Change this to either tensorflow or pytorch
                if "tensorflow" in uncleaned_value:  # <--------- Change this to either "tensorflow" or "pytorch:
                    if "\\" in uncleaned_value:
                        cleaned_value = pattern.search(uncleaned_value)
                        part_1_value = cleaned_value.group(1)
                        part_2_value = cleaned_value.group(2)
                        new_value = part_1_value +"." + part_2_value
                    else:
                        parts = uncleaned_value.split(".")
                        new_value = ".".join(parts[-3:])
                    new_value_list.append(new_value)
                elif "SMU" or "tensorflow" not in uncleaned_value:
                    new_value_list.append(uncleaned_value)

            new_dict[new_key] = new_value_list
        i = i + 1

        # writing to file stuff
        # Change this
        current_filename_extension = os.path.basename(json_graph)
        current_filename = os.path.splitext(current_filename_extension)[0]
        if "test" in current_filename:
            filename = cleaned_test_callgraph_folder + "\\" + current_filename + "_cleaned.json"
            with open(filename, 'w') as fp:
                json.dump(new_dict, fp)

        else:
            filename = cleaned_callgraph_folder + "\\" + current_filename + "_cleaned.json"
            with open(filename, 'w') as fp:
                json.dump(new_dict, fp)


def combining_callgraph(path):
    # This script combines the cleaned callgraphs into one big one

    # Your list of cleaned callgraphs
    listoffiles = glob.glob(path + "\*.json")

    print(listoffiles)

    def merge_dicts(dict1, dict2):
        for key in dict2:
            if key in dict1:
                for value in dict2[key]:
                    if value not in dict1[key]:
                        dict1[key] += [value for value in dict2[key] if value not in dict1[key]]
            else:
                # dict1[key] = dict2[key]
                dict1[key] = [value for value in dict2[key]]

    i = 1
    master_dict = {}
    for jsonfile in listoffiles:
        # print(jsonfile)
        graph = open(jsonfile)  # use with open
        a_dict = json.load(graph)
        merge_dicts(master_dict, a_dict)

    with open(final_call_graph_folder + "\\" + "final_combined_graph.json", 'w') as fp:
        json.dump(master_dict, fp)


pyCG()
cleaned_callgraph_folder = r'{}\cleaned'.format(uncleaned_call_graph_folder)  # path to be created
cleaned_test_callgraph_folder = r'{}\test'.format(cleaned_callgraph_folder)
final_call_graph_folder = r'{}\final'.format(cleaned_callgraph_folder)
try:
    os.makedirs(cleaned_callgraph_folder)
except OSError:
    pass
try:
    os.makedirs(cleaned_test_callgraph_folder)
except OSError:
    pass
cleaning()
try:
    os.makedirs(final_call_graph_folder)
except OSError:
    pass
combining_callgraph(cleaned_callgraph_folder)
