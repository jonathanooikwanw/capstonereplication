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


final_call_graph =  #the path of your final call graph, fill this in
destination_path =  #Where you want the csv files containing the vulnerable paths to end up, fill this in

#Total number of numpy functions
#Numpy example 
numpylist= ["numpy.recarray", "numpy.random.random_sample",  "numpy.concatenate","numpy.view","numpy.exp","numpy.longdouble","numpy.dtype","numpy.array","numpy.ravel_multi_index","numpy.fft.ifft","numpy.pad","numpy.random.permutation","numpy.nonzero","numpy.datetime64","numpy.fromfile","numpy.ndarray.getfield","numpy.choose","numpy.genfromtxt","numpy.histogram","numpy.random.zipf","numpy.random.dirichlet","numpy.resize","numpy.sort","numpy.apply_along_axis","numpy.polyfit","numpy.random.shuffle","numpy.flatten","numpy.reshape"]
# networkx test
f = open(final_call_graph) #<--- your final callgraph 

graph = json.load(f)

networkx_graph = nx.from_dict_of_lists(graph, create_using=nx.DiGraph) #directed graph

#PyTorch - comment out if you want to use this
for numpyfunction in numpylist:
    shortestpathlist = []
    try:
        n=nx.single_target_shortest_path(networkx_graph,numpyfunction, 4)
        for value in n.values():
            print(value)
            shortestpathlist.append(value)
    except nx.NetworkXNoPath:
        # print('No path')
        pass
    except nx.NodeNotFound:
        # print('No node' + i)
        pass
        # number = number + 1
    except KeyError:
        pass
    csvfilename = destination_path + "\\" + numpyfunction + "_networkx.csv"
    with open(csvfilename, 'w', newline='')as testfile:
        write = csv.writer(testfile)
        write.writerows(shortestpathlist)    
