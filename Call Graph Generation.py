# This script generates, pytorcgcleans, and combines call graphs 
# Example: Desktop\Work\tensorflow-master\tensorflow\python\framework\tensor_util._is_array_like -> tensor_util._is_array_like

import json
import os
import glob
import re
import pathlib
import subprocess

#takes user input from the command line to see what repository is being analyzed
repo = input("What repository are you analyzing? Lower case only please. (tensorflow or pytorch)\n")
 #Gets the path of the script
directory_of_script = pathlib.Path(__file__).parent

#Creates a new directory to contain the call graphs
uncleaned_call_graph_folder = directory_of_script / repo
try:
    os.makedirs(uncleaned_call_graph_folder)
except OSError:
    pass

# Analyze the tensorflow and pytorch repositories to obtain a call graph for every python file
def pyCG():
    # Path to your tensorflow/pytorch repository
    repo_path = input("Please provide the path to your repository.\n")
    #Obtains every python file in the repository
    python_files = glob.glob(repo_path + '/**/*.py', recursive=True)
    print("Currently processing..... This may take a while.")
    for scanned_file_name in python_files:
        #Obtains the name of the python file
        python_file_name = os.path.basename(scanned_file_name).replace('.py', '')
        #Obtains the path of the python file
        path = pathlib.PurePath(scanned_file_name)
        #Obtains the name of the folder
        folder_name = os.path.basename(path.parent)
        #Obtains the name of the parent folder
        parent_folder_name = os.path.basename(path.parent.parent)
        #Gets the call graph name where it consists of the parent folder, folder name and the python file, this is because many python files can have the same name
        call_graph_path = str(uncleaned_call_graph_folder) + "\\" + str(parent_folder_name) + "_" + str(folder_name) + "_" + str(
            python_file_name) + ".json"
        # Write to a json file
        with open(call_graph_path, 'w') as outfile:
            subprocess.run(["pycg", scanned_file_name], stdout=outfile)

# Cleans the call graphs due to pycg putting the absolute paths in the name
def cleaning():
    #gets all the json files in the uncleaned call graph folder created previously
    list_of_uncleaned_callgraphs = glob.glob(str(uncleaned_call_graph_folder) + "\*.json")
    #Regex pattern to clean the call graphs
    regex_filter_pattern = re.compile(r'([^\\]+)\\([^\\]+)$')
    print("Now cleaning.....")

    #For every json file in the folder
    for json_graph in list_of_uncleaned_callgraphs:
        #Read the json file
        f = open(json_graph)
        try:
            old_dict = json.load(f)
        except json.decoder.JSONDecodeError:
            continue

        #Create a new dictionary to hold the cleaned json file
        new_dict = {}
        #Cleaning the keys of the old call graphs
        for key in old_dict:
            new_key = ""
            new_value_list = []
            # Check if the key contains tensorflow/pytorch, if it does we want to filter it
            if repo in key:  # Change this
                # Assumption: the tensorflow keys have either \\ or not, filter accordingly Example:
                # Desktop\\Work\\tensorflow-master\\tensorflow\\python\\framework\\tensor_util._is_array_like ->
                # framework.tensor_util._is_array_like
                if "\\" in key:
                    # Use that regex filtering to perform it
                    cleaned_key = regex_filter_pattern.search(key)
                    part_1 = cleaned_key.group(1)
                    part_2 = cleaned_key.group(2)
                    new_key = part_1 + "." + part_2
                # Else split it with the dots and get the last 3 parts
                # Example: tensorflow.python.util.nest.flatten -> util.nest.flatten
                else:
                    parts = key.split(".")
                    new_key = ".".join(parts[-3:])
            else:
                new_key = key

            # Do the same cleaning on the values as the keys
            for uncleaned_value in old_dict[key]:
                if repo in uncleaned_value:
                    if "\\" in uncleaned_value:
                        cleaned_value = regex_filter_pattern.search(uncleaned_value)
                        part_1_value = cleaned_value.group(1)
                        part_2_value = cleaned_value.group(2)
                        new_value = part_1_value + "." + part_2_value
                    else:
                        parts = uncleaned_value.split(".")
                        new_value = ".".join(parts[-3:])
                    new_value_list.append(new_value)
                elif repo not in uncleaned_value:
                    new_value_list.append(uncleaned_value)
            #Fills the new dictionary with the cleaned values and keys
            new_dict[new_key] = new_value_list

        # writing to new json file, getting the name of json file
        current_filename_extension = os.path.basename(json_graph)
        current_filename = os.path.splitext(current_filename_extension)[0]

        #We want to split test and normal python files, place it in a new test folder
        if "test" in current_filename:
            filename = str(cleaned_test_callgraph_folder) + "\\" + current_filename + "_cleaned.json"
            with open(filename, 'w') as fp:
                json.dump(new_dict, fp)
        #If its a normal python file, place it in the normal folder
        else:
            filename = str(cleaned_callgraph_folder) + "\\" + current_filename + "_cleaned.json"
            with open(filename, 'w') as fp:
                json.dump(new_dict, fp)

#This function combines all the callgraphs into one big one
def combining_callgraph(cleaned_callgraph_folder):

    # Your list of cleaned callgraphs
    list_of_cleaned_callgraphs = glob.glob(str(cleaned_callgraph_folder) + "\*.json")

    #Combines the two dictionaries together
    def merge_dicts(dict1, dict2):
        for key in dict2:
            if key in dict1:
                for value in dict2[key]:
                    if value not in dict1[key]:
                        dict1[key] += [value for value in dict2[key] if value not in dict1[key]]
            else:
                dict1[key] = [value for value in dict2[key]]


    master_dict = {}
    #For every cleaned call graph, we combine it to the master dictionary
    for cleaned_callgraph in list_of_cleaned_callgraphs:
        graph = open(cleaned_callgraph)
        a_dict = json.load(graph)
        merge_dicts(master_dict, a_dict)

    with open(str(directory_of_script) + "\\" + repo + "_final_combined_graph.json", 'w') as fp:
        json.dump(master_dict, fp)


pyCG()
cleaned_callgraph_folder = uncleaned_call_graph_folder / "cleaned"
cleaned_test_callgraph_folder = cleaned_callgraph_folder / "test"

# Makes the cleaned call graph and cleaned test folders 
try:
    os.makedirs(cleaned_callgraph_folder)
except OSError:
    pass
try:
    os.makedirs(cleaned_test_callgraph_folder)
except OSError:
    pass

cleaning()

combining_callgraph(cleaned_callgraph_folder)
