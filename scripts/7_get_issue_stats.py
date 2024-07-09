from __global_paths import *
import pandas as pd

K = 200

bugs_with_stats_df = pd.merge(pd.read_csv(BUGS_WITH_TF_IDF_PATH), pd.read_csv(REPOS_PATH), left_on='repoName', right_on='nameWithOwner', how='left')
bugs_with_stats_df.to_csv(BUGS_WITH_STATS_PATH, index=False)

new_column_order = [
            "owner", "name", "title", "url_x", "fixUrl", "stars", "tf_idf", "size", "lockReason",
                "timelineCount", "labels", "fixUrlCount", "nameWithOwner", "repoName", 
                    "url_y", "description", "primaryLanguage", "updatedAt", "createdAt", "issuesCount",
                        "forkCount", "watchersCount", "discussionsCount", "id"
                        ]

bugs_with_stats_df = bugs_with_stats_df[new_column_order]

bugs_with_good_tf_idf_df = bugs_with_stats_df.sort_values(by="tf_idf", ascending=False).head(int(len(bugs_with_stats_df) * 0.2))
bugs_with_good_size_df = bugs_with_good_tf_idf_df.sort_values(by="size", ascending=False).head(int(len(bugs_with_good_tf_idf_df) * 0.5))

top_k_dfs = []

categories = ["tf_idf", "stars", "size"]
for category in categories:
    sorted_category_df = bugs_with_good_size_df.sort_values(by=category, ascending=False)
    top_k_dfs.append(sorted_category_df.head(K))

# bugs_top.tsv only includes the first 5 columns since that's what we use in the spreadsheet
bugs_from_top_in_categories = pd.concat(top_k_dfs).drop_duplicates()
bugs_from_top_in_categories.to_csv(BUGS_TOP_PATH, index=False)
bugs_from_top_in_categories[new_column_order[:5]].to_csv(BUGS_TOP_PATH[:-4]+".tsv", sep="\t", index=False)
