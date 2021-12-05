# Call graph traversal to find paths
import csv
import json
import os
import pathlib
import networkx as nx
import pandas as pd

column_names = ["Name"]

#Takes user input to get the final call graph that was created for PyTorch
final_call_graph = input("Please provide the path to your call graph for TensorFlow.\n")
final_call_graph = final_call_graph.strip('"')
# The path of your tensorflow public functions file - this is provided in the dataset
public_tensorflow_function_file = input("Please provide the path of the public TensorFlow function file.\n")
public_tensorflow_function_file = public_tensorflow_function_file.strip('"')

#Creates a new folder to hold all the paths for PyTorch
directory_of_script = pathlib.Path(__file__).parent
tensorflow_numpy_paths = directory_of_script / "tensorflow_numpy_paths"

try:
    os.makedirs(tensorflow_numpy_paths)
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
f = open(final_call_graph)

graph = json.load(f)

networkx_graph = nx.from_dict_of_lists(graph, create_using=nx.DiGraph)  

#Since we discovered all the TensorFlow public functions, we find all shortest paths from a TensorFlow public function
#to a vulnerable numpy function
df = pd.read_csv(public_tensorflow_function_file, names=column_names)
public_function_list = df.Name.to_list()
for numpy_function in numpy_list:
    shortest_path_list = []
    for public_tensorflow_function in public_function_list:
        print(public_tensorflow_function)
        try:
            paths = nx.all_shortest_paths(graph, public_tensorflow_function, numpy_function)
            for path in paths:
                shortest_path_list.append(path)
        except nx.NetworkXNoPath:
            pass
        except nx.NodeNotFound:
            pass
        except KeyError:
            pass
        
    #Writes the csv files to the folder
    csvfilename = str(tensorflow_numpy_paths) + "\\" + numpy_function + "_networkx.csv"
    with open(csvfilename, 'w', newline='')as testfile:
        write = csv.writer(testfile)
        write.writerows(shortest_path_list)
