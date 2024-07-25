import os
import subprocess
from pathlib import Path

## helper functions ##
def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

def run_command_verbose(command):
    print(" > " + command)
    out,err = run_command(command)

    if len(out) > 0:
        print("STDOUT:")
        print(out)

    if len(err) > 0:
        print("STDERR:")
        print(err)

## main ##
if __name__ == "__main__":
    # get codeql path and find relevant folders
    if "CODEQL_PATH" not in os.environ:
        print("Failed to find environment variable \"CODEQL_PATH\"")
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

    DB_path = DB_dir / DB_name # note that this variable is reassigned

    if not DB_path.exists():
        DB_path.mkdir()
    
    # run the command
    run_command_verbose(f"{CodeQL_path} database create {DB_path} --language=python --source-root={benchmark_path} --overwrite")