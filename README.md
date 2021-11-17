# An Empirical Study on Vulnerabilities in Deep Learning Librariesand Their Exploits
This is the replication package of the capstone project done by Jonathan Ooi Kwan Weng

# How to use
Each file has relevant comments and guides on where to change the variables.
##1. Call Graph Generation.py
   Change the variable path in PyCG() to the path of your TensorFlow/PyTorch repository.
   In the if statements of the cleaning() function, change the conditionals to "tensorflow" or "pytorch" depending on the repository being processed.
   Example:  if "tensorflow" in key: ->  if "pytorch" in key:
   
   This will create folders and the final callgraph in the directory of the script.
   
   PLEASE CHANGE THE NAME OF THE FOLDER BEFORE YOU RUN IT AGAIN ON A DIFFERENT REPOSITORY.
3. 
