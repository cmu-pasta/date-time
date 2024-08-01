import sys
import pandas as pd
import subprocess

from _1_generate_databases import *

QUERIES_LIST = [
    "static-analysis/deprecated_method.ql"
]

def run_query(CodeQL_path, DB_path, Query_path=Path("static-analysis/test_query.ql"), Output_loc="results/test_query.csv"):
    assert_path(DB_path)
    assert_path(Query_path)
    return run_command(f"{CodeQL_path} database analyze {DB_path} {Query_path} --output={Output_loc} --format=csv --verbose --no-rerun=false")

if __name__ == "__main__":
    CodeQL_path = get_codeql_path()
    run_benchmarks, run_repos = get_flags()

    if run_benchmarks:
        print("Running benchmarks")
        DB_path = Path("./static-analysis/databases/benchmark-db")
        print(DB_path)

        ## test query ##
        print("Running test query...")
        run_query(CodeQL_path, DB_path)

        ## test that something was found ##
        stdout, _, _ = run_command("grep -c '' results.csv")
        print(f"{stdout[:-1]} calls found")
        if (stdout == "0"):
            print("Error: No results!")
            exit(1)

        print("Passed!")



        
    if run_repos:
        print("running repos")
        print("NOT IMPLEMENTED!!!")

    
