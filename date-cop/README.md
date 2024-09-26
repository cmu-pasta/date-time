# Date-Cop

Date-Cop is an advanced tool for identifying and reporting date and time related bugs in open-source projects. It is a two part tool that utilizes static and dynamic analysis techniques to discover bugs in Python codebases.

## Features

### Static Analysis

Our static analysis approach targets Python code by traversing Abstract Syntax Trees (ASTs) derived from parsing source code. We utilize GitHub's CodeQL, a purpose-built AST query language, for discovering buggy patterns. For each identified DATE-SMELL, we develop a CodeQL query, typically consisting of about 5-20 lines of SQL-like code. This lightweight approach allows for analysis of vast amounts of code at scale, aiming to find the most bugs with the fewest false positives.

## Evaluation - GitHub Bot

DATE-COP, our GitHub bot, will leverage the GitHub API to identify active Python projects with at least 100 stars. It runs static analysis on the project's source code and executes dynamic analysis (if applicable) on the project's test executions. The bot will automatically create GitHub issues to report warnings and suggests fixes via pull requests. We will measure success based on maintainer responses, marking reports as true or false positives.

## Prerequisites

Before using Date-Cop, ensure you have the following:

1. CodeQL CLI installed on your system via the appropriate CodeQL pack
2. `CODEQL_PATH` environment variable set to your CodeQL installation directory
3. Run `code pack install` to get all python pack references

## Usage

To help with testing queries, many of the most common operations have been compiled into `run_codeql.py`. For all of the following operations, you want to be inside the `static-analysis` folder.

### Creating the CodeQL Database

To create the database for the benchmarks, run
```bash
python run_codeql.py -r
```
this creates a database in `date-cop/static-analysis/databases/benchmark-db` which the other commands can access.

### Querying the benchmarks

To run a single query `your_query_here.ql` from the `queries` folder on the benchmarks, use 
```bash
python run_codeql.py -q your_query_here
```
or, if you want to run all queries from the queries folder at once, use
```bash
python run_codeql.py -a
```
Both of these commands will create CSV files in the `results` directory with names corresponding to each query.

### Querying the repos

You can pass in a directory that contains multiple databases with `-d`. Since running a query on every repo would take way to long, use the `-n` flag to limit the number of to a smaller sample (100 or 1000 are usually good).

```bash
python run_codeql.py -a -d ./databases_path -rp ./path_to_results -n 100
```

### Manual Querying

If you're more familiar with CodeQL or need to run your queries from another location, the following commands can be used to create a database and run a query on it respectively. (Assuming you are in the `/date-cop` folder).

Step 1: Create a CodeQL database
```bash
codeql database create ./static-analysis/databases/<name of your db> --language=python --source-root=<original code directory>
```
Commands which analyse multiple databases (which these do most of the time) will create an output in `results/your_query_here_merged.csv` and will include a database column on the left.

Step 2: Run queries on the database
```bash
codeql database analyze ./static-analysis/databases/<name of your db> <path to your query>.ql --output=results.csv --format=csv --verbose --rerun --download
```

