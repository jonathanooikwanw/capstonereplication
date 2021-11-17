# An Empirical Study on Vulnerabilities in Deep Learning Librariesand Their Exploits
This is the replication package of the capstone project done by Jonathan Ooi Kwan Weng

# How to use
Each file has relevant comments and guides on where to change the variables.
## Call Graph Generation.py
   Change the variable path in PyCG() to the path of your TensorFlow/PyTorch repository.
   
   In the if statements of the cleaning() function, change the conditionals to "tensorflow" or "pytorch" depending on the repository being processed.
   Example:  if "tensorflow" in key: ->  if "pytorch" in key:
   
   This will create folders and the final callgraph in the directory of the script.
   
   PLEASE CHANGE THE NAME OF THE FOLDER BEFORE YOU RUN IT AGAIN ON A DIFFERENT REPOSITORY.

## Discovering_public_function_paths.py
   Fill in the variables final_call_graph and destination_path, there are comments explaining the variables.
   1. For TensorFlow:
      Fill in the variables tfpublicfunctionspath with the path of the tensorflowpublicfunctions.csv file.
   2. For PyTorch:
      Just run as is, commenting out the TensorFlow part
      
## Exploit code
   For both TensorFlow and PyTorch, the NumPy version used is 1.17 for numpy.array and numpy.dtype.
   TensorFlow numpy.load uses TensorFlow version 2.20 and NumPy version 1.16.
   TensorFlow version used is Tensorflow 2.3.1
   
