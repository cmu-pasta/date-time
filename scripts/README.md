# Data Gathering Scripts

This directory contains the scripts used to generate our dataset.

## Our computed data

 - all\_repos\_with\_stats.csv: contains all repos gathered from 0\_find\_repos.py and statistics about them from GitHub.
 - all\_repos\_with\_loc.csv: contains a copy of the content from all\_repos\_with\_stats.csv with an additional python lines of code column.
 - repos\_with\_separated\_grep.csv: contains the grep results of each repository (i.e., whether it contains "import datetime", "import arrow", etc., or similar)
 - issues.csv: contains all the issues found by searching for specific key-words among only the repositories containing a datetime import (see repos\_with\_separated\_grep.csv)
 - bugs.csv: contains all issues.csv lines that contain the keyword "bug", "fix", or similar.

## Usage

First, create at least one GitHub access token. Copy each access token into `access_tokens` and title the files `gh_access_token_[0 .. #number of access tokens]`.

Modify `num_gh_keys` in `3_get_bugs.sh` to match the number of GitHub access tokens you added in the previous step.

Run the data-gathering scripts:

```sh
python3 0_find_repos.py
python3 1_get_repos.py
python3 2_get_repo_statistics.py
./3_get_bugs.sh
python3 4_get_bug_statistics.py
python3 5_get_tf_idf.py
```
