import sys
import subprocess
import pandas as pd

sys.path.append('../scripts')

from __global_paths import *

df = pd.read_csv(DT_REPOS_PATH)

subprocess.run(f"mkdir -p {CODEQL_DBS_DIR}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

for i, row in df.iterrows():
    path = CLONE_REPOS_DIR + row["owner"] + "+" + row["name"]
    db_path = CODEQL_DBS_DIR + row["owner"] + "+" + row["name"]
    result = subprocess.run(f"codeql database create {db_path} --language=python --source-root={path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(f"{i}: {path}")
