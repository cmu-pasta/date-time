from __global_paths import *
import pandas as pd

bugs_df = pd.read_csv(BUGS_PATH)
repos_df = pd.read_csv(SEPARATED_FILTERED_REPOS_PATH)

repos_df["nameWithOwner"] = repos_df["owner"] + "/" + repos_df["name"]
counts = bugs_df['repoName'].value_counts().reset_index()
counts["nameWithOwner"] = counts["repoName"]

result = pd.merge(repos_df, counts, on='nameWithOwner', how='left')

print(len(bugs_df))
print({
    'datetime': int(result[result['grep_results0'] > 0]['count'].sum()),
    'arrow': int(result[result['grep_results1'] > 0]['count'].sum()),
    'pendulum': int(result[result['grep_results2'] > 0]['count'].sum()),
    'whenever': int(result[result['grep_results3'] > 0]['count'].sum())
})

print(bugs_df["repoName"].nunique())
print({
    'datetime': (result[result['grep_results0'] > 0]['count'] > 0).sum(),
    'arrow': (result[result['grep_results1'] > 0]['count'] > 0).sum(),
    'pendulum': (result[result['grep_results2'] > 0]['count'] > 0).sum(),
    'whenever': (result[result['grep_results3'] > 0]['count'] > 0).sum()
})
