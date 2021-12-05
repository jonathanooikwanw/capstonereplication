# Call graph traversal to find paths
import json
import csv
import networkx as nx
import pathlib
import os

#Takes user input to get the final call graph that was created for PyTorch
final_call_graph = input("Please provide the path to your call graph for PyTorch.\n")
final_call_graph = final_call_graph.strip('"')
cutoff = int(input("Please input the cutoff of the paths you want (max length of paths).\n"))

#Creates a new folder to hold all the paths for PyTorch
directory_of_script = pathlib.Path(__file__).parent
pytorch_numpy_paths = directory_of_script / "pytorch_numpy_paths"
try:
    os.makedirs(pytorch_numpy_paths)
except OSError:
    pass


# Total number of numpy functions we discovered when labeling the silent fixes, these functions are deemed to be vulnerable
numpy_list = ["numpy.recarray", "numpy.random.random_sample", "numpy.concatenate", "numpy.view", "numpy.exp",
              "numpy.longdouble", "numpy.dtype", "numpy.array", "numpy.ravel_multi_index", "numpy.fft.ifft",
              "numpy.pad", "numpy.random.permutation", "numpy.nonzero", "numpy.datetime64", "numpy.fromfile",
              "numpy.ndarray.getfield", "numpy.choose", "numpy.genfromtxt", "numpy.histogram", "numpy.random.zipf",
              "numpy.random.dirichlet", "numpy.resize", "numpy.sort", "numpy.apply_along_axis", "numpy.polyfit",
              "numpy.random.shuffle", "numpy.flatten", "numpy.reshape"]

#Loads and converts the final call graph to a networkx graph
f = open(final_call_graph)  # <--- your final callgraph

graph = json.load(f)

networkx_graph = nx.from_dict_of_lists(graph, create_using=nx.DiGraph)  

#For every vulnerable numpy function, use it as the target and find all the shortest paths to it from a pytorch function
#We assume every pytorch function is public since its too difficult to find them
for numpy_function in numpy_list:
    shortest_path_list = []
    try:
        n = nx.single_target_shortest_path(networkx_graph, numpy_function, cutoff)
        for value in n.values():
            print(value)
            shortest_path_list.append(value)
    except nx.NetworkXNoPath:
        pass
    except nx.NodeNotFound:
        pass
    except KeyError:
        pass

    #Writes the csv files to the folder
    csvfilename = str(pytorch_numpy_paths) + "\\" + numpy_function + "_networkx.csv"
    with open(csvfilename, 'w', newline='')as testfile:
        write = csv.writer(testfile)
        write.writerows(shortest_path_list)
