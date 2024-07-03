from __global_paths import *
import pandas as pd

bugs_with_stats_df = pd.merge(pd.read_csv(BUGS_WITH_TF_IDF_PATH), pd.read_csv(REPOS_PATH), left_on='repoName', right_on='nameWithOwner', how='left')

bugs_with_stats_df.to_csv(BUGS_WITH_STATS_PATH, index=False)
