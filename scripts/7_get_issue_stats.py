from __global_paths import *
import pandas as pd

K = 200
SIZE_MIN = 1000

# bugs_with_stats_df = pd.merge(pd.read_csv(BUGS_WITH_TF_IDF_PATH), pd.read_csv(REPOS_PATH), left_on='repoName', right_on='nameWithOwner', how='left')
# bugs_with_stats_df.to_csv(BUGS_WITH_STATS_PATH, index=False)

bugs_df = pd.read_csv(BUGS_WITH_TF_IDF_PATH)
repos_df = pd.read_csv(REPOS_PATH)
grep_results_df = pd.read_csv(REPOS_WITH_GREP_PATH)

# filter out enchancements
mask = []
for i,row in bugs_df.iterrows():
    if "enhancement" in str(row):
        mask.append(False)
    else:
        mask.append(True)

print("Removing", sum([0 if e else 1 for e in mask]), "enhancements")
bugs_df = bugs_df[mask]

# Merge the first two DataFrames
bugs_with_stats_df = pd.merge(bugs_df, repos_df, left_on='repoName', right_on='nameWithOwner', how='left')
bugs_with_stats_df = pd.merge(bugs_with_stats_df, grep_results_df, on='nameWithOwner', how='left')

# Save the final DataFrame to a CSV file
bugs_with_stats_df.to_csv(BUGS_WITH_STATS_PATH, index=False)

new_column_order = ["owner_x", "name_x", "title", "url_x", "fixUrl", "stars", "tf_idf", "size", "grep_results0", "grep_results1", "grep_results2"]

bugs_with_stats_df = bugs_with_stats_df[new_column_order]

bugs_with_good_size_df = bugs_with_stats_df[bugs_with_stats_df["size"] >= SIZE_MIN]
bugs_with_good_tf_idf_df = bugs_with_good_size_df.sort_values(by="tf_idf", ascending=False).head(int(len(bugs_with_good_size_df) * 0.2))

top_k_dfs = []

categories = ["tf_idf", "stars", "size"]
for category in categories:
    sorted_category_df = bugs_with_good_tf_idf_df.sort_values(by=category, ascending=False)
    top_k_dfs.append(sorted_category_df.head(K))

# bugs_top.tsv only includes the first 5 columns since that's what we use in the spreadsheet
bugs_from_top_in_categories = pd.concat(top_k_dfs).drop_duplicates()
bugs_from_top_in_categories.to_csv(BUGS_TOP_PATH, index=False)
bugs_from_top_in_categories.to_csv(BUGS_TOP_PATH[:-4]+".tsv", sep="\t", index=False)
