__ALL__ = ['structure', 'components', 'gui']
__AUTHOR__ = "Evening Programmer"
__VERSION__ = "1.0.0"

import os, sys

# Set the starting point to the directory containing the script
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_directory)

# Move up two directories to reach the parent directory (AOSS)
parent_directory = os.path.abspath(os.path.join(script_directory, '..'))
sys.path.append(parent_directory)


from main import *