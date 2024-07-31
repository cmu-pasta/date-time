import sys
import subprocess
import pandas as pd

sys.path.append('../scripts')

from __global_paths import *

df = pd.read_csv(REPOS_WITH_GREP_PATH)

count = 0

for i, repo in df.iterrows():
    if (repo["grep_results0"] == 0 and repo["grep_results1"] == 0 and repo["grep_results2"] == 0):
        count += 1

print(f"DELETING {count} REPOS!")

for i, repo in df.iterrows():
    if (repo["grep_results0"] == 0 and repo["grep_results1"] == 0 and repo["grep_results2"] == 0):
        repo_path = f"{CLONE_REPOS_DIR}{repo['owner'] + '+' + repo['name']}"
        subprocess.run(f"rm -rf {repo_path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
