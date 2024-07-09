from __global_paths import *
import pandas as pd

K = 200

bugs_with_stats_df = pd.merge(pd.read_csv(BUGS_WITH_TF_IDF_PATH), pd.read_csv(REPOS_PATH), left_on='repoName', right_on='nameWithOwner', how='left')
bugs_with_stats_df.to_csv(BUGS_WITH_STATS_PATH, index=False)

bugs_with_good_tf_idf_df = bugs_with_stats_df.sort_values(by="tf_idf", ascending=False).head(int(len(bugs_with_stats_df) * 0.2))
bugs_with_good_size_df = bugs_with_good_tf_idf_df.sort_values(by="size", ascending=False).head(int(len(bugs_with_stats_df) * 0.8))

top_k_dfs = []

categories = ["tf_idf", "stars", "size"]
for category in categories:
    sorted_category_df = bugs_with_good_size_df.sort_values(by=category, ascending=False)
    top_k_dfs.append(sorted_category_df.head(K))

bugs_from_top_in_categories = pd.concat(top_k_dfs).drop_duplicates()
bugs_from_top_in_categories.to_csv(BUGS_TOP_PATH, index=False)
