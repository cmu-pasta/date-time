from __global_paths import *
import pandas as pd
import subprocess

keyword_lines_len = 5

issue_dfs = []
bug_dfs = []

for i in range(keyword_lines_len):
    issue_dfs.append(pd.read_csv(ISSUES_PATH + f"_{i}"))
    bug_dfs.append(pd.read_csv(BUGS_PATH + f"_{i}"))

issues_df = pd.concat(issue_dfs).drop_duplicates()
bugs_df = pd.concat(bug_dfs).drop_duplicates()

issues_df.to_csv(CONCAT_ISSUES_PATH)
bugs_df.to_csv(CONCAT_BUGS_PATH)

repos_df = pd.read_csv(SEPARATED_FILTERED_REPOS_PATH)
repos_df["nameWithOwner"] = repos_df["owner"] + "/" + repos_df["name"]
counts = bugs_df['repoName'].value_counts().reset_index()
counts["nameWithOwner"] = counts["repoName"]

result = pd.merge(repos_df, counts, on='nameWithOwner', how='left')

print(f"NUM_BUGS: {len(bugs_df)}")
print({
    'datetime': int(result[result['grep_results0'] > 0]['count'].sum()),
    'arrow': int(result[result['grep_results1'] > 0]['count'].sum()),
    'pendulum': int(result[result['grep_results2'] > 0]['count'].sum()),
    'whenever': int(result[result['grep_results3'] > 0]['count'].sum())
})

print(f"NUM_BUGGY_REPOS: {bugs_df['repoName'].nunique()}")
print({
    'datetime': (result[result['grep_results0'] > 0]['count'] > 0).sum(),
    'arrow': (result[result['grep_results1'] > 0]['count'] > 0).sum(),
    'pendulum': (result[result['grep_results2'] > 0]['count'] > 0).sum(),
    'whenever': (result[result['grep_results3'] > 0]['count'] > 0).sum()
})

words="""
datetime	pytz	leap	strptime	microsecond
timestamp	dateutil	DST	strftime	nanosecond
tzinfo	arrow	daylight	utcnow	millisecond
epoch	pendulum	year	fromtimestamp	timezone
timedelta	UTC	localtime	GMT	interval
fold	elapsed	duration	
""".split()

print(f"NUM_WORDS: {len(words)}")

#issue_word_counts = {}
bug_word_counts = dict()

for word in words:
    bug_word_counts[word] = 0
    #issue_count = int(subprocess.run(f"grep -cE '{word}' {CONCAT_ISSUES_PATH}", shell=True, check=True).stdout)
    bug_count = int(subprocess.run(f"grep -cE '\\b{word}\\b' {CONCAT_BUGS_PATH}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout)
    #issue_word_counts[word] += issue_count
    bug_word_counts[word] += bug_count

#print(issue_word_counts)
print(bug_word_counts)
    
