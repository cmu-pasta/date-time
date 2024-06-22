import pandas as pd
from __global_paths import *

repos_with_grep_paths = [
        "repos_with_separated_grep_multigrep_0_2000.csv",
        "repos_with_separated_grep_multigrep_2000_4000.csv",
        "repos_with_separated_grep_multigrep_4000_6000.csv",
        "repos_with_separated_grep_multigrep_6000_8000.csv",
        "repos_with_separated_grep_multigrep_8000_10000.csv",
        "repos_with_separated_grep_multigrep_10000_12000.csv",
        "repos_with_separated_grep_multigrep_12000_14000.csv",
        "repos_with_separated_grep_multigrep_14000_16000.csv",
        "repos_with_separated_grep_multigrep_16000_18000.csv",
        "repos_with_separated_grep_multigrep_18000_20000.csv",
        "repos_with_separated_grep_multigrep_20000_22000.csv",
        ]

dfs = []
for csv in repos_with_grep_paths:
        dfs.append(pd.read_csv(DATA_DIR + csv))

ret_df = pd.concat(dfs)
ret_df.to_csv(SEPARATED_FILTERED_REPOS_PATH, index=False)