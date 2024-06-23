from __global_paths import *
import pandas as pd

data = pd.read_csv(SEPARATED_FILTERED_REPOS_PATH)
print(len(data[data['grep_results0'] == 0]))
print(len(data[data['grep_results0'] == 1]))