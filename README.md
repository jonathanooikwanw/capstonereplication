# Analyzing Vulnerabilities in Deep Learning Libraries and Their Exploits
This is the replication package of the capstone project done by Jonathan Ooi Kwan Weng

# How to use
Each file has relevant comments and guides on where to change the variables.

## Call Graph Generation.py
   This file takes two user inputs.
   1. The name of the repository to be scanned (tensorflow or pytorch) in **lower** case.
   2. The path to the repository to be scanned. (Example: C:\Users\User\Desktop\Work\tensorflow-master)
   
   It will perform three actions.
   1. Create a call graph from every python file in the repository.
   2. Clean the keys and values of the call graphs. (Example: Desktop\Work\tensorflow-master\tensorflow\python\framework\tensor_util.\_is_array_like -> tensor_util.\_is_array_like). This is because PyCG takes the absolute paths of the files and functions.
   3. Combines all the cleaned call graphs into one large call graph.

## Discovering_public_function_paths_tensorflow.py
   This file takes two user inputs.
   1. The path of the final call graph for TensorFlow. You can get this by doing (shift+right click) on the final TensorFlow call graph. Ensure your input has quotation marks. (Example: "C:\Users\User\Desktop\Replication Package\tensorflow_final_combined_graph.json")
   2. The path of the public TensorFlow function csv file provided in the dataset. Do the same steps as step 1. (Example: "C:\Users\User\Desktop\Replication Package\tensorflowpublicfunctions.csv").

## Discovering_public_function_paths_pytorch.py
   This file takes two user inputs. We do not have the public functions of PyTorch as it was too difficult to obtain. Therefore, we assume all functions are public.
   1. The path of the final call graph for TensorFlow. You can get this by doing (shift+right click) on the final TensorFlow call graph. Ensure your input has quotation marks. (Example: "C:\Users\User\Desktop\Replication Package\pytorch_final_combined_graph.json")
   2. The maximum length/cutoff of the shortest paths obtained. 
   
## Call graph versions
   The call graphs of TensorFlow are created from TensorFlow version 2.6.0.
   The call graphs of PyTorch are created from PyTorch version 1.9.0.

## Exploit code
   For both TensorFlow and PyTorch, the NumPy version used is 1.17 for numpy.array and numpy.dtype.
   TensorFlow numpy.load uses TensorFlow version 2.20 and NumPy version 1.16.
   TensorFlow version used is Tensorflow 2.3.1
   You can install the specific numpy version commit using this command.
   ``pip install git+git://github.com/numpy/numpy.git@d121225b410628d71be8626057c0540c2053c965``
   
## Reference repositories
   https://github.com/vitsalis/PyCG
