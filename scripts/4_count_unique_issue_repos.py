import pandas as pd
from __global_paths import *

print(pd.read_csv(ISSUES_PATH)["repoName"].nunique())