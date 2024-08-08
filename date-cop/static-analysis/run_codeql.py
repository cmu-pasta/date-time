import argparse
import os
import subprocess
from pathlib import Path

QL_DIR = "./queries/"
RS_DIR = "./results/"
DB_PATH = Path("./databases/benchmark-db")
BENCHMARKS_PATH = Path("../../benchmarks")
CODEQL_PATH = ""
QUERIES_LIST = [
    "delta_divide",
    "delta_times_float",
    "deprecated_method",
    "tz_equals_none",
    "multiple_nows",
    "timezone_offset",
    "bad_pytz_init",
]


def run_command(command):
    print(f"\nRunning command: {command}")
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return result


def set_codeql_path():
    global CODEQL_PATH
    if "CODEQL_PATH" in os.environ:
        CodeQL_dir = Path(os.environ["CODEQL_PATH"])
        CodeQL_path = os.path.join(CodeQL_dir, "codeql")
    else:
        print("CODEQL_PATH is not set")
        exit(1)

    CODEQL_PATH = CodeQL_path


def run_query(Query_path, Output_path):
    return run_command(
        f"{CODEQL_PATH} database analyze {DB_PATH} {Query_path} --output={Output_path} --format=csv --verbose --rerun"
    )

def run_named_query(query):
    print(f"Running query {query} for database {DB_PATH}")
    
    if not os.path.exists(RS_DIR):
        os.makedirs(RS_DIR)

    q_path = os.path.join(QL_DIR, query + ".ql")
    out_path = os.path.join(RS_DIR, query + ".csv")
    result = run_query(q_path, out_path)
    if result.returncode != 0:
        print(f"Error found with database {DB_PATH} and query {q_path}:\n{result}")
        exit(1)


def run_all_queries():
    print(f"Running all queries for database {DB_PATH}")

    if not os.path.exists(RS_DIR):
        os.makedirs(RS_DIR)

    for query in QUERIES_LIST:
        q_path = os.path.join(QL_DIR, query + ".ql")
        out_path = os.path.join(RS_DIR, query + ".csv")
        result = run_query(q_path, out_path)
        if result.returncode != 0:
            print(f"Error found with database {DB_PATH} and query {q_path}:\n{result}")
            exit(1)


def create_db():
    print("Creating benchmark database...")

    if not DB_PATH.exists():
        os.makedirs(DB_PATH)

    return run_command(
        f"{CODEQL_PATH} database create {DB_PATH} --language=python --source-root={BENCHMARKS_PATH} --overwrite"
    )


def main():
    parser = argparse.ArgumentParser(description="Run CodeQL queries on benchmarks.")
    parser.add_argument(
        "--recreate",
        "-r",
        action="store_true",
        help="Recreate the benchmarks database.",
    )
    parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        help="Run all queries on the benchmarks database.",
    )
    parser.add_argument(
        "--one",
        "-o",
        help="Run a single specified query.",
    )

    args = parser.parse_args()
    set_codeql_path()

    if args.recreate or not DB_PATH.exists():
        create_db()

    if args.all:
        run_all_queries()
    
    if args.one is not None:
        run_named_query(args.one)


if __name__ == "__main__":
    main()
