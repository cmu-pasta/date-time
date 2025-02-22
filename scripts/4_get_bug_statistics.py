from __global_paths import *
import pandas as pd
import subprocess

issue_dfs = []
bug_dfs = []

for i in range(KEYWORDS_LIST_LEN):
    issue_dfs.append(pd.read_csv(PARTIAL_ISSUES_DIR + f"{i}"))
    bug_dfs.append(pd.read_csv(PARTIAL_BUGS_DIR + f"{i}"))

issues_df = pd.concat(issue_dfs).drop_duplicates()
bugs_df = pd.concat(bug_dfs).drop_duplicates()
bugs_fixed_df = bugs_df[pd.notna(bugs_df["fixUrl"])]
bugs_fixed_df = bugs_fixed_df[bugs_fixed_df.iloc[:, -1] != "fixUrlCount"]

issues_df.to_csv(ISSUES_PATH, index=False)
bugs_df.to_csv(BUGS_PATH, index=False)
bugs_fixed_df.to_csv(BUGS_WITH_FIXES_PATH, index = False)

repos_df = pd.read_csv(DT_REPOS_PATH)

repos_df["nameWithOwner"] = repos_df["owner"] + "/" + repos_df["name"]
counts = bugs_df['repoName'].value_counts().reset_index()
counts["nameWithOwner"] = counts["repoName"]

result = pd.merge(repos_df, counts, on='nameWithOwner', how='left')

print(f"NUM_BUGS: {len(bugs_df)}")
print({
    'datetime': int(result[result['grep_results0'] > 0]['count'].sum()),
    'arrow': int(result[result['grep_results1'] > 0]['count'].sum()),
    'pendulum': int(result[result['grep_results2'] > 0]['count'].sum())
})

print(f"NUM_BUGGY_REPOS: {bugs_df['repoName'].nunique()}")
print({
    'datetime': (result[result['grep_results0'] > 0]['count'] > 0).sum(),
    'arrow': (result[result['grep_results1'] > 0]['count'] > 0).sum(),
    'pendulum': (result[result['grep_results2'] > 0]['count'] > 0).sum()
})

print(f"NUM_WORDS: {len(KEYWORDS_RAW)}")

for word in KEYWORDS_RAW:
    #issue_count = int(subprocess.run(f"grep -icE '{word}' {ISSUES_PATH}", shell=True, check=True).stdout)
    bug_count = int(subprocess.run(f"grep -icE '{word}' {BUGS_PATH}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout)
    #issue_word_counts[word] += issue_count
    # bug_word_counts[word] += bug_count
    print(word.ljust(14)+str(bug_count))

