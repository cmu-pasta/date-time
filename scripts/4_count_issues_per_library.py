from __global_paths import *
import pandas as pd

# Load the CSV files
bugs_df = pd.read_csv(BUGS_PATH)
repos_df = pd.read_csv(SEPARATED_FILTERED_REPOS_PATH)

# Display the first few rows of each dataframe to understand their structure
bugs_df.head(), repos_df.head()

# Merge the dataframes on the repository name
# Create a column in bugs_df to match the format in repos_df for merging
bugs_df['repoNameFormatted'] = bugs_df['repoName'].apply(lambda x: x.split('/')[-1])

# Merge the dataframes
merged_df = pd.merge(bugs_df, repos_df, left_on='repoNameFormatted', right_on='name', how='inner')

# Now, we will count the number of issues for each repository based on the grep results
grep_counts = merged_df.groupby(['name', 'grep_results0', 'grep_results1', 'grep_results2', 'grep_results3']).size().reset_index(name='issue_count')

# Sum the number of issues for each grep result category
# Group by repo and grep results, then count the issues
issue_counts = merged_df.groupby(['name', 'grep_results0', 'grep_results1', 'grep_results2', 'grep_results3']).size().reset_index(name='issue_count')

# Sum the number of issues for each grep result category
grep_summary = {
    'grep_results0': issue_counts[issue_counts['grep_results0'] > 0]['issue_count'].sum(),
    'grep_results1': issue_counts[issue_counts['grep_results1'] > 0]['issue_count'].sum(),
    'grep_results2': issue_counts[issue_counts['grep_results2'] > 0]['issue_count'].sum(),
    'grep_results3': issue_counts[issue_counts['grep_results3'] > 0]['issue_count'].sum()
}

print(grep_summary)

# Load the CSV files
bugs_df = pd.read_csv(BUGS_PATH)
repos_df = pd.read_csv(SEPARATED_FILTERED_REPOS_PATH)

# Create a column in bugs_df to match the format in repos_df for merging
bugs_df['repoNameFormatted'] = bugs_df['repoName'].apply(lambda x: x.split('/')[-1])

# Merge the dataframes
merged_df = pd.merge(bugs_df, repos_df, left_on='repoNameFormatted', right_on='name', how='inner')

# Group by repository and grep results, then count unique repositories
unique_repos = merged_df.groupby(['name', 'grep_results0', 'grep_results1', 'grep_results2', 'grep_results3']).size().reset_index(name='issue_count')

# Check if a repository uses each grep result
grep_summary_repos = {
    'grep_results0': unique_repos[unique_repos['grep_results0'] > 0]['name'].nunique(),
    'grep_results1': unique_repos[unique_repos['grep_results1'] > 0]['name'].nunique(),
    'grep_results2': unique_repos[unique_repos['grep_results2'] > 0]['name'].nunique(),
    'grep_results3': unique_repos[unique_repos['grep_results3'] > 0]['name'].nunique()
}

print(bugs_df["repoName"].nunique())

print(grep_summary_repos)