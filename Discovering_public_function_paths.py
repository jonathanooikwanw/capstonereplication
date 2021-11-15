#Call graph traversal to find paths
import ast
import astunparse
import os
import networkx as nx
import json
import csv
import glob
import pandas as pd
import pathlib

column_names = ["Name"]
df = pd.read_csv(r'C:\Users\User\Desktop\Work\SMU\Capstone\Datasets\callgraph\Tensorflow Call Graphs\publicfunctions2.csv', names=column_names) #The path of your tensorflow public functions file - this is provided in the dataset
publicfunctionlist = df.Name.to_list()
final_call_graph = #the path of your final call graph
destination_path = #Where you want the csv files containing the vulnerable paths to end up

#Total number of numpy functions
#Numpy example 
numpylist= ["numpy.recarray", "numpy.random.random_sample",  "numpy.concatenate","numpy.view","numpy.exp","numpy.longdouble","numpy.dtype","numpy.array","numpy.ravel_multi_index","numpy.fft.ifft","numpy.pad","numpy.random.permutation","numpy.nonzero","numpy.datetime64","numpy.fromfile","numpy.ndarray.getfield","numpy.choose","numpy.genfromtxt","numpy.histogram","numpy.random.zipf","numpy.random.dirichlet","numpy.resize","numpy.sort","numpy.apply_along_axis","numpy.polyfit","numpy.random.shuffle","numpy.flatten","numpy.reshape"]
# networkx test
f = open(final_call_graph) #<--- your final callgraph 

graph = json.load(f)

networkx_graph = nx.from_dict_of_lists(graph, create_using=nx.DiGraph) #directed graph

for numpyfunction in numpylist:
    # shortest_path = nx.all_shortest_paths(networkx_graph, "tensor_util.is_tf_type", "numpy.concatenate")
    shortestpathlist = []
    for i in publicfunctionlist:
        print(i)
        try:
            n=nx.all_shortest_paths(graph,i,numpyfunction)
            for a in n:
                shortestpathlist.append(a)
        except nx.NetworkXNoPath:
            # print('No path')
            pass
        except nx.NodeNotFound:
            # print('No node' + i)
            pass
            # number = number + 1
        except KeyError:
            pass
    print(shortestpathlist)
    csvfilename = destination_path + "\\" + numpyfunction + "_networkx.csv"
    with open(csvfilename, 'w', newline='')as testfile:
        write = csv.writer(testfile)
        write.writerows(shortestpathlist)    
