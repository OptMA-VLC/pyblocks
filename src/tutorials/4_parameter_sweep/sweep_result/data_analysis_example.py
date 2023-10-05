# Sample data analysis script for parameter sweep result
from .load_result import load_result

# load results from the data.pkl file
sweep_result = load_result('./data.pkl')

# do your analysis using the sweep_result object
print(sweep_result)
