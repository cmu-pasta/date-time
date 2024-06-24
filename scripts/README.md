# Data Gathering Scripts

## Table of Contents

1. [Introduction](#introduction)
2. [Requirements](#requirements)
4. [Usage](#usage)
5. [Command-Line Checks](#command-line-checks)

## Introduction

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

```sh
python3 0_find_repos.py
python3 1_get_repos.py
python3 2_get_issues.py
python3 3_get_issues_statistics.py
```

## Command-Line Checks

Check that all repos are cloned:

```sh
find . -type d -empty | wc -l
```