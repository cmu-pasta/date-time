from __global_paths import *
import pandas as pd

K = 100

bugs_with_stats_df = pd.merge(pd.read_csv(BUGS_WITH_TF_IDF_PATH), pd.read_csv(REPOS_PATH), left_on='repoName', right_on='nameWithOwner', how='left')

bugs_with_stats_df.to_csv(BUGS_WITH_STATS_PATH, index=False)

categories = ["stars", "tf_idf", "timelineCount", "issuesCount", "forkCount", "watchersCount", "discussionsCount"]


top_k_dfs = []

for category in categories:
    sorted_category_df = bugs_with_stats_df.sort_values(by=category, ascending=False)
    top_k_dfs.append(sorted_category_df.head(K))

bugs_from_top_in_categories = pd.concat(top_k_dfs).drop_duplicates()
bugs_from_top_in_categories.to_csv(BUGS_TOP_PATH, index=False)
