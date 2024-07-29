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
    run_command(f"{codeql_path} database create {db_path} --language=python --source-root={source_path} --overwrite")


## main ##
if __name__ == "__main__":
    # get codeql path
    if "CODEQL_PATH" not in os.environ:
        print("Failed to find environment variable \"CODEQL_PATH\"")
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

    CodeQL_dir = Path(os.environ["CODEQL_PATH"])
    CodeQL_path = CodeQL_dir / "codeql"
    benchmark_path = Path("./benchmarks")
    DB_dir = Path("./date-cop/static-analysis/databases")
    DB_name = "benchmark-db"
    if not benchmark_path.exists():
        print(f"failed to find folder {benchmark_path}, make sure you're in the /date-time folder.")
        exit(1)

    if not DB_dir.exists():
        print(f"failed to find folder {DB_dir}, make sure you're in the /date-time folder.")
        exit(1)

    DB_path = DB_dir / DB_name

    if not DB_path.exists():
        DB_path.mkdir()
    
    # run the command
    run_command_verbose(f"{CodeQL_path} database create {DB_path} --language=python --source-root={benchmark_path} --overwrite")