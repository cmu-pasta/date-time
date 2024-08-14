import os
import subprocess
import pandas as pd
from pathlib import Path
import argparse
import csv

from __global_paths import *

STRING_OPS_PATH = DATA_DIR+"string_operations.csv"
# DT_REPOS_PATH
# CLONE_REPOS_DIR

"""
Table Schema:
owner     - repo owner
repo      - repo name
path      - relative path within the repo
line      - linenumber
operation - "parse" or "format"
text      - content of the line
"""

P_PATTERNS = [
    "strptime",
    "to_datetime",
    "arrow.get", # this is a catch all constructor and so likely has false positives. (see https://arrow.readthedocs.io/en/latest/api-guide.html#arrow.factory.ArrowFactory.get) 
    "pendulum.parse",
    "maya.parse",
    "dateparser.parse",
    "dateutil.parser.parse",
]

F_PATTERNS = [
    "strftime",
    "isoformat",
    "ctime",
    # not included in here is the potential to use str(dt) or format strings
]

def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

def find_matches(path, patterns):
    command = "grep -nw "
    command += " ".join([f"-e \"{p}\"" for p in patterns])
    command += f" \"{path}\""
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
    ans = []
    for line in result.stdout.split("\n"):
        if len(line) == 0:
            continue
        try:
            semicolon = line.index(":")
            line_num = int(line[:semicolon])
            ans.append((line_num, line[semicolon+1:]))
        except Exception as e:
            print(f"Skipping {path} - exception in parsing grep:")
            print(e)
            return []
    return ans

def count_python_lines(repo_owner, repo_name):
    repo_path = os.path.join(CLONE_REPOS_DIR, f"{repo_owner}+{repo_name}")
    stdout, stderr = run_command(f"find {repo_path} -name '*.py' | xargs wc -l")
    total_lines = sum(int(line.split()[0]) for line in stdout.splitlines() if line.split())
    return total_lines

def search_repo(owner, name):
    cloned = Path(CLONE_REPOS_DIR) / (owner+"+"+name)
    assert cloned.exists()
    py_files = cloned.rglob("*.py")
    loc = count_python_lines(owner, name)
    results = []
    if loc > 1000000:
        print(f"Skipping {owner}/{name} - too many lines of code ({loc})")
        return []
    
    for f in py_files:
        relpath = str(f.relative_to(cloned))
        if "test" in relpath:
            # print(f"Skipping {f} - testfile")
            continue

        matches = find_matches(f, F_PATTERNS)
        for match in matches:
            results.append({
                "path":      relpath,
                "line":      match[0],
                "operation": "format",
                "text":      match[1]
            })

        matches = find_matches(f, P_PATTERNS)
        for match in matches:
            results.append({
                "path":      relpath,
                "line":      match[0],
                "operation": "parse",
                "text":      match[1]
            })
    return results

def search_all_repos(dest):
    with open(dest, "w") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["owner", "repo", "path", "line", "operation", "text"])

        dt_repos = pd.read_csv(DT_REPOS_PATH)
        total_rows = dt_repos.shape[0]
        for i, row in dt_repos.iterrows():
            for result in search_repo(row["owner"], row["name"]):
                writer.writerow([
                    row["owner"], row["name"],
                    result["path"], result["line"],
                    result["operation"], result["text"]
                ])
            if i%500 == 0:
                print(f"finished {row['owner']}/{row['name']}, {i} of {total_rows}")
            

if __name__ == "__main__":
    search_all_repos(STRING_OPS_PATH)
