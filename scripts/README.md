# Data Gathering Scripts

This directory contains the scripts used to generate our dataset.

## Requirements

- python3
- pandas
- requests
- json
- csv

## Usage

First, create a GitHub access token. Copy its contents into the file `access_tokens/gh_access_token`.

Run the data-gathering scripts:

## Our computed data

 - all\_repos\_with\_stats.csv: contains all repos gathered from 0\_find\_repos.py and statistics about them from GitHub.
 - all\_repos\_with\_loc.csv: contains a copy of the content from all\_repos\_with\_stats.csv with an additional python lines of code column.
 - repos\_with\_separated\_grep.csv: contains the grep results of each repository (i.e., whether it contains "import datetime", "import arrow", etc., or similar)
 - issues.csv: contains all the issues found by searching for specific key-words among only the repositories containing a datetime import (see repos\_with\_separated\_grep.csv)
 - bugs.csv: contains all issues.csv lines that contain the keyword "bug", "fix", or similar.

```sh
python3 0_find_repos.py
python3 1_get_repos.py
python3 2_get_bugs.py
python3 3_get_bug_statistics.py
```

## Command-Line Checks

Check that all repos are cloned:

```sh
find . -type d -empty | wc -l
```
