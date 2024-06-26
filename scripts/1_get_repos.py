import os
import subprocess
import pandas as pd
import shutil
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

from __global_paths import *

MAX_RETRIES = 5
BACKOFF_FACTOR = 2

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

def git_clone(repo_owner, repo_name, retries=MAX_RETRIES, backoff_factor=BACKOFF_FACTOR):
    repo_path = f"{repo_owner}:{repo_name}"
    
    if os.path.exists(os.path.join(CLONE_REPOS_DIR, repo_path)):
        return "Repository already exists, skipping clone.", "", True
    
    for attempt in range(retries):
        stdout, stderr = run_command(f"git clone --depth 1 https://github.com/{repo_owner}/{repo_name} {os.path.join(CLONE_REPOS_DIR, repo_path)}")
        if "fatal" not in stderr:
            return stdout, stderr, True
        time.sleep(backoff_factor ** attempt)
    return stdout, stderr, False

def grep_repo(repo_owner, repo_name):
    repo_path = os.path.join(CLONE_REPOS_DIR, f"{repo_owner}:{repo_name}")
    stdout0, _ = run_command(f"grep --include=\*.py -rE '^\s*(import.*|from)\s+datetime' {repo_path}")
    stdout1, _ = run_command(f"grep --include=\*.py -rE '^\s*(import.*|from)\s+arrow' {repo_path}")
    stdout2, _ = run_command(f"grep --include=\*.py -rE '^\s*(import.*|from)\s+pendulum' {repo_path}")
    stdout3, _ = run_command(f"grep --include=\*.py -rE '^\s*(import.*|from)\s+whenever' {repo_path}")
    stdout4, _ = run_command(f"grep --include=\*.py -rE '^\s*(import.*|from)\s+heliclockter' {repo_path}")
    return (1 if stdout0 else 0, 1 if stdout1 else 0, 1 if stdout2 else 0, 1 if stdout3 else 0, 1 if stdout4 else 0)

def count_python_lines(repo_owner, repo_name):
    repo_path = os.path.join(CLONE_REPOS_DIR, f"{repo_owner}:{repo_name}")
    stdout, stderr = run_command(f"find {repo_path} -name '*.py' | xargs wc -l")
    total_lines = sum(int(line.split()[0]) for line in stdout.splitlines() if line.split())
    return total_lines

def process_repo(repo_owner, repo_name, logger):
#    repo_path = os.path.join(CLONE_REPOS_DIR, f"{repo_owner}:{repo_name}")
#    clone_stdout, clone_stderr, success = git_clone(repo_owner, repo_name)
#    if not success:
#        logger.error(f"Failed to clone repository {repo_owner}/{repo_name} after {MAX_RETRIES} attempts.")
#        return pd.DataFrame()

    grep_result = grep_repo(repo_owner, repo_name)
    # loc = count_python_lines(repo_owner, repo_name)

    return pd.DataFrame({
        "nameWithOwner": [repo_owner + "/" + repo_name],
        "owner": [repo_owner],
        "name": [repo_name],
        "grep_results0": [grep_result[0]],
        "grep_results1": [grep_result[1]],
        "grep_results2": [grep_result[2]],
        "grep_results3": [grep_result[3]],
        "grep_results4": [grep_result[4]]
        # "loc": [loc]
    })

def process_repos(df, logger):
    df_curs = []
    for i, row in df.iterrows():
        repo_owner = row['owner']
        repo_name = row['name']
        df_curs.append(process_repo(repo_owner, repo_name, logger))
        logger.info(f"Processed repository {repo_owner}/{repo_name}")
    df_ret = pd.concat(df_curs, ignore_index=True)
    return df_ret

def main():
    print("STARTING REPO FILTERING")
    df = pd.read_csv(REPOS_PATH)
    if not os.path.exists(CLONE_REPOS_DIR):
        os.makedirs(CLONE_REPOS_DIR)

    from_index = 0 if (len(sys.argv) == 1) else int(sys.argv[1])
    to_index = len(df) if (len(sys.argv) == 1) else int(sys.argv[2])

    logger = setup_logger(f"thread_{from_index}_{to_index}", CLONE_REPOS_DIR + f"thread_{from_index}_{to_index}")
    df_ret = process_repos(df[from_index:to_index], logger)

    ret_path = SEPARATED_FILTERED_REPOS_PATH if len(sys.argv) == 1 else f"{SEPARATED_FILTERED_REPOS_PATH[:-4]}_multigrep_{from_index}_{to_index}.csv"
    df_ret.to_csv(ret_path, index=False)
    
    run_command(f"head -n 1 {ret_path} > {ret_path[:-4] + '_filtered.csv'}")
    run_command(f"grep ',1,' {ret_path} >> {ret_path[:-4] + '_filtered.csv'}")
    
if __name__ == "__main__":
    main()
