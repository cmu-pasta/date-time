import os
import subprocess
import pandas as pd
import shutil
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

from __global_paths import *

contains_funcs_df = pd.read_csv(REPOS_WITH_GREP_FUNCS_PATH)
issues_w_stats_df = pd.read_csv(BUGS_WITH_STATS_PATH)

merged_df = pd.merge(contains_funcs_df, issues_w_stats_df, on="nameWithOwner", how="inner")

agg_dict = {keyw: "first" for keyw in keyws}
agg_dict["tf_idf"] = "sum"
agg_dict["stars"] = "first"
agg_dict["size"] = "first"


result_df = merged_df.groupby(["nameWithOwner", "name", "owner"]).agg(agg_dict).reset_index()
result_df['bug_count'] = merged_df.groupby(["nameWithOwner", "name", "owner"])['tf_idf'].transform('count')

sorted_df = result_df.sort_values(by="tf_idf", ascending=False)

sorted_df.to_csv(REPOS_WITH_FUNCS_STATS_PATH, index=False)

for keyw in keyws:
    filtered_df = sorted_df[sorted_df[keyw] == 1]
    filtered_df.to_csv(FUNCS_GREP_DIR + keyw, index=False)
