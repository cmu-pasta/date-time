import sys
import subprocess
import pandas as pd

sys.path.append('../scripts')

from __global_paths import *

print(DATA_DIR)

df = pd.read_csv(DT_REPOS_PATH)
#df = pd.read_csv(REPOS_PATH)

print(df)

subprocess.run(f"mkdir -p {CODEQL_DBS_DIR}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

for i, row in df.iterrows():
    #old_path = CLONE_REPOS_DIR + row["owner"] + "\:" + row["name"]
    path = CLONE_REPOS_DIR + row["owner"] + "+" + row["name"]
    db_path = CODEQL_DBS_DIR + row["owner"] + "+" + row["name"]
    #print(path)
    #print(db_path)

    """
    result = subprocess.run(f"mv -f {old_path} {path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)
    print(result.stderr)
    """

    result = subprocess.run(f"codeql database create {db_path} --language=python --source-root={path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(f"{i}: {path}")
    """
    print(result.stdout)
    print(result.stderr)
    if i > 0:
        break
    """
