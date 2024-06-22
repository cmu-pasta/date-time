import pandas as pd
from __global_paths import *

repos_with_grep_paths = [
        "repos_with_grep_and_loc_0_5000.csv",
        "repos_with_grep_and_loc_5000_10000.csv",
        "repos_with_grep_and_loc_10000_15000.csv",
        "repos_with_grep_and_loc_15000_20000.csv",
        "repos_with_grep_and_loc_20000_25000.csv",
        "repos_with_grep_and_loc_25000_30000.csv",
        "repos_with_grep_and_loc_30000_35000.csv",
        "repos_with_grep_and_loc_35000_40000.csv",
        "repos_with_grep_and_loc_40000_45000.csv",
        "repos_with_grep_and_loc_45000_50000.csv",
        "repos_with_grep_and_loc_50000_55000.csv",
        "repos_with_grep_and_loc_55000_60000.csv"
        ]

dfs = []
for csv in repos_with_grep_paths:
        dfs.append(pd.read_csv(DATA_DIR + csv))

ret_df = pd.concat(dfs)
ret_df.to_csv(FILTERED_REPOS_PATH, index=False)

datetime_repos = ret_df[ret_df["grep_results"] != 0]

datetime_repos.to_csv(DATETIME_REPOS_PATH, index=False)
