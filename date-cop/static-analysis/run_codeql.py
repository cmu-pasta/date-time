import argparse
import os
import subprocess
import random
from pathlib import Path

QL_DIR = "./queries/"
RS_DIR = "./results/"
DEFAULT_DB_PATH = Path("./databases/benchmark-db")
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
    "bad_pytz_init_var",
    "partial_replace",
]


def run_command(command):
    print(f"Running command: {command}\n")
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


def run_query(db_path, query_path, output_path):
    return run_command(
        f"{CODEQL_PATH} database analyze {db_path} {query_path} --output={output_path} --format=csv --verbose --rerun"
    )


def run_all_queries(db_path):
    if not os.path.exists(RS_DIR):
        os.makedirs(RS_DIR)

    for query in QUERIES_LIST:
        print(f"Running {query} for database {db_path}")
        q_path = os.path.join(QL_DIR, query + ".ql")
        out_path = os.path.join(RS_DIR, query + "_" + db_path.parts[-1] + ".csv")
        result = run_query(db_path, q_path, out_path)
        if result.returncode != 0:
            print(f"Error found with database {db_path} and query {q_path}:\n{result}")
            exit(1)


def clean_merged_files():
    for query in QUERIES_LIST:
        merged_path = Path(RS_DIR, query + "_merged.csv")
        if merged_path.exists():
            run_command(f"rm -f {merged_path}")


def merge_results_for_query(query):
    global ouputs
    ouputs = [
        Path(RS_DIR, query + "_" + db_path.parts[-1] + ".csv") for db_path in DB_PATHS
    ]
    merged = open(Path(RS_DIR, query + "_merged.csv"), "w")
    for output in ouputs:
        out = open(output, "r")
        for line in out.readlines():
            merged.write(line)


def merge_results():
    for query in QUERIES_LIST:
        merge_results_for_query(query)

def randompaths(base, count, seed):
    if type(base) != Path:
        base = Path(base)
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
        "--query",
        "-q",
        type=str,
        help="Run a single specified query.",
    )
    parser.add_argument("--dbpath", "-dp", type=str, help="Run on a set of databases.")
    parser.add_argument(
        "--number", "-n", type=int, help="Run on specified number of databases."
    )
    parser.add_argument(
        "--seed", type=int, default=123456, help="Set the random seed for -n"
    )
    parser.add_argument(
        "--norandom", action="store_true", default=False, help="don't shuffle and instead take the first n arguments with `-n`"
    )
    parser.add_argument(
        "--resultpath",
        "-rp",
        type=str,
        help="Path to store the results of the queries.",
    )
    return parser


def main():
    args = init_parser().parse_args()
    set_codeql_path()

    global DB_PATHS
    if args.dbpath is not None:
        if args.number is not None:
            if args.norandom:
                DB_PATHS = [p for p in Path(args.dbpath).iterdir()][: args.number]
            else:
                DB_PATHS = randompaths(args.dbpath, args.number, args.seed)
        else:
            DB_PATHS = [p for p in Path(args.dbpath).iterdir()]
    else:
        DB_PATHS = [DEFAULT_DB_PATH]

    if args.recreate or not DEFAULT_DB_PATH.exists():
        create_db()

    if args.query is not None:
        global QUERIES_LIST
        QUERIES_LIST = [args.query]

    if args.resultpath is not None:
        global RS_DIR
        RS_DIR = args.resultpath

    if len(DB_PATHS) > 1:
        clean_merged_files()

    for db_path in DB_PATHS:
        run_all_queries(db_path)

    if len(DB_PATHS) > 1:
        merge_results()


if __name__ == "__main__":
    main()
