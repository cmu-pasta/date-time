import sys
import pandas as pd
import subprocess

from _1_generate_databases import *

QL_DIR = "static-analysis/"
RS_DIR = "results/"

QUERIES_LIST = [
    "delta_divide",
    "delta_times_float",
    "deprecated_method",
    "multiple_nows",
    "timezone_offset"
]

def run_query(CodeQL_path, DB_path, Query_path=Path("static-analysis/test_query.ql"), Output_path="results/test_query.csv"):
    assert_path(DB_path)
    assert_path(Query_path)
    return run_command(f"{CodeQL_path} database analyze {DB_path} {Query_path} --output={Output_path} --format=csv --verbose --no-rerun=false")

def run_all_queries(CodeQL_path, DB_path):
    print(f"Running all queries for database {DB_path}")
    for q in QUERIES_LIST:
        q_path = Path(QL_DIR + q + ".ql")
        out_path = Path(RS_DIR + q + ".csv")
        ret = run_query(CodeQL_path, DB_path, Query_path=q_path, Output_path=out_path)
        if ret[2] != 0:
            print(f"Error found with database {DB_path} and query {q_path}:\n{ret}")
            exit(1)

def test_query(CodeQL_path, DB_path):
    run_query(CodeQL_path, DB_path)
 
    assert_path(Path("results/test_query.csv"))
    stdout, _, _ = run_command("grep -c '' results/test_query.csv")

    if (stdout == "0\n"):
        print("Error: No results!")
        exit(1)

if __name__ == "__main__":
    CodeQL_path = get_codeql_path()
    run_benchmarks, run_repos = get_flags()

    if run_benchmarks:
        DB_path = Path("./static-analysis/databases/benchmark-db")
        test_query(CodeQL_path, DB_path)
        run_all_queries(CodeQL_path, DB_path)
        
    if run_repos:
        print("running repos")
        print("NOT IMPLEMENTED!!!")

    
