# Date-Cop

Date-Cop is an advanced tool for identifying and reporting date and time related bugs in open-source projects. It is a two part tool that utilizes static and dynamic analysis techniques to discover bugs in Python codebases.

## Features

### Static Analysis

Our static analysis approach targets Python code by traversing Abstract Syntax Trees (ASTs) derived from parsing source code. We utilize GitHub's CodeQL, a purpose-built AST query language, for discovering buggy patterns. For each identified DATE-SMELL, we develop a CodeQL query, typically consisting of about 5-20 lines of SQL-like code. This lightweight approach allows for analysis of vast amounts of code at scale, aiming to find the most bugs with the fewest false positives.

### Dynamic Analysis

For bug patterns that cannot be described in terms of syntax alone, we employ dynamic analysis. This method implements monkey-patching of library data structures, replacing classes like `datetime` with appropriate subclasses that perform dynamic checks. The analysis raises warnings when problematic bug patterns are encountered during operations, acting as a form of dynamic linting specialized to date and time operations. These dynamic analyses are applied to open-source projects via GitHub Actions, hooking into normal unit test and integration test execution.

## Evaluation - GitHub Bot

DATE-COP, our GitHub bot, will leverage the GitHub API to identify active Python projects with at least 100 stars. It runs static analysis on the project's source code and executes dynamic analysis (if applicable) on the project's test executions. The bot will automatically create GitHub issues to report warnings and suggests fixes via pull requests. We will measure success based on maintainer responses, marking reports as true or false positives.

## Prerequisites

Before using Date-Cop, ensure you have the following:

1. CodeQL CLI installed on your system via the appropriate CodeQL pack
2. `CODEQL_PATH` environment variable set to your CodeQL installation directory

## Usage

### Creating a CodeQL Database

To create a CodeQL database for the Python benchmarks, run the following command:

```bash
codeql database create ./date-cop/static-analysis/databases/<name of your db> --language=python --source-root=./benchmarks/
```

### Running the Analysis

To run the CodeQL analysis using the Date-Cop query, use this command:

```bash
codeql database analyze ./date-cop/static-analysis/databases/<name of your db> ./date-cop/static-analysis/<name of your query>.ql --output=results.csv --format=csv --verbose --no-rerun=false
```
