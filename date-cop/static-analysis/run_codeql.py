import argparse
import os
import subprocess
from pathlib import Path

VERBOSE = True
QL_DIR = "./queries/"
RS_DIR = "./results/"
DEFAULT_DB_PATH = Path("./databases/benchmark-db")
DB_PATHS = []
BENCHMARKS_PATH = Path("../../benchmarks")
CODEQL_PATH = ""
QUERIES_LIST = [
    "DeprecatedMethodCall",
    "PartialReplace",
    "NaiveDatetimeCreation",
    "BadPytzTimezoneInit",
    "RelativedeltaDivide",
    "FixedOffsetTimezone",
    "SubtractingDatetimes",
]


def pretty_print(message, indent=0):
    if VERBOSE:
        if indent == 0:
            print("=" * 20 + "\n" + message + "\n" + "=" * 20)
        else:
            print("  " * indent + "\\_" + message)


def run_command(command):
    pretty_print(f"Running command: {command}\n", 1)
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
        pretty_print("CODEQL_PATH is not set")
        exit(1)

    CODEQL_PATH = CodeQL_path


def create_db():
    pretty_print("Creating benchmark database...")

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
        pretty_print(f"Running {query} for database {db_path}")
        q_path = os.path.join(QL_DIR, query + ".ql")
        out_path = os.path.join(RS_DIR, query + "_" + db_path.parts[-1] + ".csv")
        result = run_query(db_path, q_path, out_path)
        if result.returncode != 0:
            pretty_print(f"Error found with database {db_path} and query {q_path}", 1)
            exit(1)


def merge_results_for_query(query):
    pretty_print(f"Merging results for query {query}.\n", 1)

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
    pretty_print("Merging results.")
    for query in QUERIES_LIST:
        merge_results_for_query(query)


def clean_merged_files():
    pretty_print("Cleaning up files.")

    for query in QUERIES_LIST:
        for db_path in DB_PATHS:
            out_path = Path(RS_DIR, query + "_" + db_path.parts[-1] + ".csv")
            if out_path.exists():
                run_command(f"rm -f {out_path}")
            else:
                pretty_print(f"Skipping cleanup as {out_path} does not exist.\n", 1)


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
        default=None,
        help="Run a single specified query.",
    )
    parser.add_argument(
        "--dbpath",
        "-dp",
        type=str,
        help="Run on a set of databases.",
    )
    parser.add_argument(
        "--number",
        "-n",
        type=int,
        help="Run on specified number of databases.",
    )
    parser.add_argument(
        "--resultpath",
        "-rp",
        type=str,
        help="Path to store the results of the queries.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print verbose output.",
    )
    return parser


def main():
    args = init_parser().parse_args()

    global VERBOSE
    VERBOSE = args.verbose

    set_codeql_path()

    if args.recreate or not DEFAULT_DB_PATH.exists():
        create_db()

    global DB_PATHS
    if args.dbpath is not None:
        DB_PATHS = [Path(args.dbpath, p) for p in os.listdir(args.dbpath)]
        if args.number is not None and args.number < len(DB_PATHS):
            DB_PATHS = DB_PATHS[: args.number]
    else:
        DB_PATHS = [DEFAULT_DB_PATH]

    if args.all:
        pass
    elif not args.all and args.query is not None:
        global QUERIES_LIST
        QUERIES_LIST = [args.query]
    else:
        pretty_print("Not running any queries.")
        return

    if args.resultpath is not None:
        global RS_DIR
        RS_DIR = args.resultpath

    for db_path in DB_PATHS:
        run_all_queries(db_path)

    if len(DB_PATHS) > 1:
        merge_results()
        clean_merged_files()


if __name__ == "__main__":
    main()
