import os
import sys
import subprocess
from pathlib import Path
import pandas as pd

## helper functions ##
def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

def create_db(codeql_path, db_path, source_path):
    run_command(f"\"{codeql_path}\" database create {db_path} --language=python --source-root={source_path} --overwrite")

def assert_path(path, error_hint = ""):
    if not path.exists():
        error_msg = f"Failed to find path {path}."
        if len(error_hint) != 0:
            error_msg += " " + error_hint
        print(error_msg)
        exit(1)

## main ##
if __name__ == "__main__":
    # get codeql path
    if "CODEQL_PATH" in os.environ:
        CodeQL_dir = Path(os.environ["CODEQL_PATH"])
        print("tesion1", CodeQL_dir.exists())
        CodeQL_path = CodeQL_dir / "codeql"
        assert_path(CodeQL_path)
    else:
        CodeQL_path = "codeql"
    
    # test if codeql path works
    shell_test = subprocess.run(f"\"{CodeQL_path}\" version -v", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if shell_test.returncode != 0:
        print("failed to run codeql")
        print(f"ERR: {shell_test.stderr}")
        exit(1)
    
    # get command line args
    if len(sys.argv) == 1:
        generate_benchmarks = True
        generate_repos = False
    else:
        generate_benchmarks = "--benchmarks" in sys.argv
        generate_repos = "--repos" in sys.argv
        if not (generate_benchmarks or generate_repos):
            print(f"Usage: {sys.argv[0]} [--benchmarks] [--repos]")
            print("If no flag is provided, default to --benchmarks")
            exit(1)

    # benchmarks
    if generate_benchmarks:
        print("Creating Benchmarks")
        benchmark_path = Path("../benchmarks")
        DB_dir = Path("./static-analysis/databases")
        print(DB_dir)
        DB_name = "benchmark-db"
        DB_path = DB_dir / DB_name

        assert_path(benchmark_path, "Make sure you're in the date-time/date-cop folder.")
        assert_path(DB_dir, "Make sure you're in the date-time/date-cop folder.")
        if not DB_path.exists():
            DB_path.mkdir()
        
        # run the command
        create_db(CodeQL_path, DB_path, benchmark_path)
    
    # repos
    if generate_repos:
        sys.path.append('../scripts')
        from __global_paths import *

        assert_path(Path(DT_REPOS_PATH))
        assert_path(Path(CODEQL_DBS_DIR))
        assert_path(Path(CLONE_REPOS_DIR))

        df = pd.read_csv(DT_REPOS_PATH)
        for i, row in df.iterrows():
            path = CLONE_REPOS_DIR + row["owner"] + "+" + row["name"]
            print(f"{i}: {path}")
            db_path = CODEQL_DBS_DIR + row["owner"] + "+" + row["name"]
            create_db(CodeQL_path, db_path, path)
