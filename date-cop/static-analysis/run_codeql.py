import argparse
import os
import subprocess
import random
from pathlib import Path

QL_DIR = "./queries/"
RS_DIR = "./results/"
DEFAULT_DB_PATH = Path("./databases/benchmark-db")
SELECT_DB_PATH = Path("/data/sjoukov/date-time/data/codeql_databases")
DB_PATHS = []
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

def create_db():
    print("Creating benchmark database...")

    if not DEFAULT_DB_PATH.exists():
        os.makedirs(DEFAULT_DB_PATH)

    return run_command(
        f"{CODEQL_PATH} database create {DEFAULT_DB_PATH} --language=python --source-root={BENCHMARKS_PATH} --overwrite"
    )

def run_query(db_path, Query_path, Output_path):
    return run_command(
        f"{CODEQL_PATH} database analyze {db_path} {Query_path} --output={Output_path} --format=csv --verbose --rerun"
    )

def run_named_query(db_path, query):
    print(f"Running query {query} for database {db_path}")
    
    if not os.path.exists(RS_DIR):
        os.makedirs(RS_DIR)

    q_path = os.path.join(QL_DIR, query + ".ql")
    out_path = os.path.join(RS_DIR, query + ".csv")
    result = run_query(db_path, q_path, out_path)
    if result.returncode != 0:
        print(f"Error found with database {db_path} and query {q_path}:\n{result}")
        exit(1)

def run_all_queries(db_path):
    print(f"Running all queries for database {db_path}")

    if not os.path.exists(RS_DIR):
        os.makedirs(RS_DIR)

    for query in QUERIES_LIST:
        q_path = os.path.join(QL_DIR, query + ".ql")
        out_path = os.path.join(RS_DIR, query + ".csv")
        result = run_query(db_path, q_path, out_path)
        if result.returncode != 0:
            print(f"Error found with database {db_path} and query {q_path}:\n{result}")
            exit(1)

def clean_merged_files():
    for query in QUERIES_LIST:
        merged_path = Path(RS_DIR, query + "_merged.csv")
        if merged_path.exists():
            run_command(f"rm -f {merged_path}")

def merge_results(db_name):
    for query in QUERIES_LIST:
        out_path = Path(RS_DIR, query + ".csv")
        merged_path = Path(RS_DIR, query + "_merged.csv")
        if out_path.exists():
            out = open(out_path, "r")
            merged = open(merged_path, "a")
            for line in out.readlines():
                merged.write(f"{db_name},"+line)

def randompaths(base, count, seed):
    rng = random.Random(seed)
    paths = [p for p in base.iterdir()]
    rng.shuffle(paths)
    return paths[:count]

def init_parser():
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
    parser.add_argument(
        "--databases",
        "-d",
        nargs="+",
        help="Run on specified databases"
    )
    parser.add_argument(
        "--select",
        "-s",
        type=int,
        help="Run on specified number of random databases."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default="125600",
        help="Random seed (for use with --select)."
    )
    return parser

def main():
    args = init_parser().parse_args()
    set_codeql_path()

    global DB_PATHS
    if args.databases:
        DB_PATHS = [Path(db) for db in args.databases]
    elif args.select is not None:
        DB_PATHS = randompaths(SELECT_DB_PATH, args.select, args.seed)
    else:
        DB_PATHS = [DEFAULT_DB_PATH]
    
    if args.recreate or not DEFAULT_DB_PATH.exists():
        create_db()
    
    if len(DB_PATHS) > 1:
        clean_merged_files()

    for db_path in DB_PATHS:
        if args.all:
            run_all_queries(db_path)
        elif args.one is not None:
            run_named_query(db_path, args.one)

        if len(DB_PATHS) > 1:
            merge_results(db_path.stem)


if __name__ == "__main__":
    main()
