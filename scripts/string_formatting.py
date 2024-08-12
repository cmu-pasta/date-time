import os
import subprocess
import pandas as pd
from pathlib import Path
import argparse

from __global_paths import *

STRING_OPS_PATH = DATA_DIR+"string_operations.csv"
# DT_REPOS_PATH
# CLONE_REPOS_DIR

"""
Table Schema:
repo      - [owner]+[reponame]
path      - relative path within the repo
line      - linenumber
pattern   - pattern id
operation - "parse" or "format"
text      - content of the line
"""

P_PATTERNS = [
    "strptime",
    "to_datetime",
    "arrow.get",
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

def searchrepo(owner, name):
    cloned = Path(CLONE_REPOS_DIR) / (owner+"+"+name)
    assert cloned.exists()

if __name__ == "__main__":
    #https://github.com/census-instrumentation/opencensus-python/issues/547
    searchrepo("census-instrumentation", "opencensus-python")
