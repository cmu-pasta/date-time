import os
import subprocess
import pandas as pd
import shutil
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

from global_paths import *

# Constants
NUM_THREADS = 16
MAX_RETRIES = 5
BACKOFF_FACTOR = 2

# Setup logging
if not os.path.exists(CLONE_REPOS_DIR):
    os.makedirs(CLONE_REPOS_DIR)

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
    stdout0, _ = run_command(f"timeout 10s grep --include=\*.py -rE '^\s*(import.*|from\s*)(datetime|arrow|pendulum|whenever)' {repo_path}")
    # return (1 if stdout0 else 0, 1 if stdout1 else 0, 1 if stdout2 else 0, 1 if stdout3 else 0)
    return 1 if stdout0 else 0

def count_python_lines(repo_owner, repo_name):
    return 1
    repo_path = os.path.join(CLONE_REPOS_DIR, f"{repo_owner}:{repo_name}")
    stdout, stderr = run_command(f"find {repo_path} -name '*.py' | xargs wc -l")
    total_lines = sum(int(line.split()[0]) for line in stdout.splitlines() if line.split())
    return total_lines

def delete_repo_contents(repo_owner, repo_name):
    return
    # repo_path = os.path.join(CLONE_REPOS_DIR, f"{repo_owner}:{repo_name}")
    # for item in os.listdir(repo_path):
    #     item_path = os.path.join(repo_path, item)
    #     if os.path.isdir(item_path):
    #         shutil.rmtree(item_path)
    #     else:
    #         os.remove(item_path)

def get_dir_size(path, logger):
    return 1
    # total = 0
    # with os.scandir(path) as it:
    #     for entry in it:
    #         try:
    #             if entry.is_symlink():
    #                 logger.warning(f"Skipping symbolic link: {entry.path}")
    #                 continue
    #             if entry.is_file():
    #                 total += entry.stat().st_size
    #             elif entry.is_dir():
    #                 total += get_dir_size(entry.path, logger)
    #         except OSError as e:
    #             logger.error(f"Error accessing {entry.path}: {str(e)}")
    #             continue
    # return total

def process_repo(repo_owner, repo_name, logger):
    # repo_path = os.path.join(CLONE_REPOS_DIR, f"{repo_owner}:{repo_name}")
    # clone_stdout, clone_stderr, success = git_clone(repo_owner, repo_name)
    # if not success:
    #     logger.error(f"Failed to clone repository {repo_owner}/{repo_name} after {MAX_RETRIES} attempts.")
    #     return pd.DataFrame()

    grep_result = grep_repo(repo_owner, repo_name)
    # loc = count_python_lines(repo_owner, repo_name)
    # repo_size = get_dir_size(repo_path, logger)
    
    # if repo_size > 1 * 1024 * 1024 * 1024:  # 1 GB
        # delete_repo_contents(repo_owner, repo_name)

    return pd.DataFrame({
        "owner": [repo_owner],
        "name": [repo_name],
        "grep_results": [grep_result],
        # "grep_results0": [grep_result[0]],
        # "grep_results1": [grep_result[1]],
        # "grep_results2": [grep_result[2]],
        # "grep_results3": [grep_result[3]],
        # "loc": [loc],
        # "size": [repo_size]
    })
    
    # return pd.DataFrame()

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
    print("STARTING")
    
    # Load DataFrame
    df = pd.read_csv(REPOS_PATH)

    # Initialize columns with correct types
    df['grep_results0'] = 0
    df['grep_results1'] = 0
    df['grep_results2'] = 0
    df['grep_results3'] = 0
    df['loc'] = 0
    df['size'] = 0

    # Create the directory to store cloned repos if it doesn't exist
    if not os.path.exists(CLONE_REPOS_DIR):
        os.makedirs(CLONE_REPOS_DIR)

    # Create indices for splitting the DataFrame
    # len_each = len(df) // NUM_THREADS
    # indices = [(len_each * i, len(df) if i == NUM_THREADS - 1 else len_each * (i + 1)) for i in range(NUM_THREADS)]

    # indices = [(i*10, i*10 + 10) for i in range(10)]

    # print(indices)

    from_index = 0 if (len(sys.argv) == 1) else int(sys.argv[1])
    to_index = len(df) if (len(sys.argv) == 1) else int(sys.argv[2])

    logger = setup_logger(f"thread_{from_index}_{to_index}", CLONE_REPOS_DIR + f"thread_{from_index}_{to_index}")
    df_ret = process_repos(df[from_index:to_index], logger)
    df_ret.to_csv(f"{FILTERED_REPOS_PATH[:-4]}_{from_index}_{to_index}.csv", index=False)

    
    exit(0)
    
    # Process each repo using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = {}
        loggers = {}
        df_ret = pd.DataFrame()
        
        for thread_id, (start_index, end_index) in enumerate(indices):
            logger = setup_logger(f"thread_{thread_id}", os.path.join(CLONE_REPOS_DIR, f"thread_{thread_id}.log"))
            loggers[thread_id] = logger
            df_cur = df.loc[start_index:end_index]
            futures[executor.submit(process_repos, df_cur, start_index, end_index, logger, thread_id)] = thread_id

        for future in as_completed(futures):
            thread_id = futures[future]
            try:
                df_cur = future.result()  # Correct method name
                df_cur.to_csv(DATA_DIR + f"{thread_id}.csv", index=False)
                print(f"thread {thread_id}, len: {len(df_cur)}")
                df_ret = pd.concat([df_ret, df_cur], ignore_index=True)
            except Exception as e:
                loggers[thread_id].error(f"Error processing process: {str(e)}")

    # Save the updated DataFrame to a new CSV file
    df_ret.to_csv(FILTERED_REPOS_PATH, index=False)

if __name__ == "__main__":
    main()
