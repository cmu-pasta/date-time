import os
import subprocess
import pandas as pd
import shutil
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

from __global_paths import *

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

def grep_repo(repo_owner, repo_name):
    repo_path = os.path.join(CLONE_REPOS_DIR, f"{repo_owner}+{repo_name}")
    stdouts = []
    for keyw in keyws:
        stdout, _ = run_command(f"grep -m 1 --include=*.py -rE '{keyw}' {repo_path}")
        stdouts.append(stdout)

    return [1 if stdout else 0 for stdout in stdouts]

def count_python_lines(repo_owner, repo_name):
    repo_path = os.path.join(CLONE_REPOS_DIR, f"{repo_owner}+{repo_name}")
    stdout, stderr = run_command(f"find {repo_path} -name '*.py' | xargs wc -l")
    total_lines = sum(int(line.split()[0]) for line in stdout.splitlines() if line.split())
    return total_lines

def process_repo(repo_owner, repo_name, logger):
    grep_result = grep_repo(repo_owner, repo_name)

    return pd.DataFrame({
        "nameWithOwner": [repo_owner + "/" + repo_name],
        "owner": [repo_owner],
        "name": [repo_name],
        **{f"{keyws[i]}": [grep_result[i]] for i in range(len(grep_result))}
    })

def process_repos(df, logger):
    df_curs = []
    for i, row in df.iterrows():
        #if (i == 50): break
        repo_owner = row['owner']
        repo_name = row['name']
        df_curs.append(process_repo(repo_owner, repo_name, logger))
        logger.info(f"Processed repository {repo_owner}/{repo_name}")
    df_ret = pd.concat(df_curs, ignore_index=True)
    return df_ret

def main():
    df = pd.read_csv(DT_REPOS_PATH)
    if not os.path.exists(CLONE_REPOS_DIR):
        os.makedirs(CLONE_REPOS_DIR)

    logger = setup_logger("get_repos_with_specific_funcs", LOG_PATH)
    df_ret = process_repos(df, logger)

    df_ret.to_csv(REPOS_WITH_GREP_FUNCS_PATH, index=False)
    
if __name__ == "__main__":
    main()
