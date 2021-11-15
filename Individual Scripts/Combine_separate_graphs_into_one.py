
import json
import glob

#This script combines the cleaned callgraphs into one big one

#Your list of cleaned callgraphs
cleaned_callgraph_path = #THIS IS WHERE YOUR CLEANED CALLGRAPHS FOLDER PATH IS AFTER YOU RUN CALLGRAPH_CLEANING.PY
listoffiles = glob.glob(cleaned_callgraph_path + "\*.json")
final_callgraph_path = # THIS IS WHERE YOU WANT YOUR FINAL CALLGRAPH TO END UP
name_of_final_callgraph = #name of your final call graph, fill this in

print(len(listoffiles))

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
    print(i)
    # print(jsonfile)
    graph = open(jsonfile)# use with open
    a_dict = json.load(graph)
    merge_dicts(master_dict, a_dict)

with open(final_callgraph_path + name_of_final_callgraph + ".json", 'w') as fp: # THE DESTINATION OF YOUR FINAL CALLGRAPH
   json.dump(master_dict, fp)


