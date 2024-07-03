DATA_DIR = "/data/sjoukov/date-time/data/"

LOG_PATH = DATA_DIR + "log"

KEYWORDS_RAW = """
datetime    nanosecond  strptime    timezone    elapsed
pytz    millisecond strftime    timezones   interval
dateutil    microsecond timestamp   GMT intervals
arrow   second  utcnow  UTC duration
pendulum    seconds fromtimestamp   DST 
tzinfo  day localtime   daylight    
days    timedelta   fold    
week        leap    
weeks
month
months
year
years
epoch
""".split()
KEYWORDS_LIST_LEN = 7

KEYWORDS = []
for start in range(0, len(KEYWORDS_RAW), 6): KEYWORDS.append(KEYWORDS_RAW[start:start+6])
KEYWORDS_WITH_OR = [" OR ".join(KEYWORDS[i]) for i in range(len(KEYWORDS))]

NUM_GH_ACCESS_TOKENS = 7

GH_ACCESS_TOKEN = "access_tokens/gh_access_token"
SG_ACCESS_TOKEN = "access_tokens/sg_access_token"

CLONE_REPOS_DIR = DATA_DIR + "cloned_repos/"

REPOS_PATH = DATA_DIR + "repos.csv"
REPOS_WITH_GREP_PATH = DATA_DIR + "repos_w_grep.csv"
DT_REPOS_PATH = DATA_DIR + "dt_repos.csv"
# "GREPPOS"

PARTIAL_ISSUES_DIR = DATA_DIR + "partial_issues/"
PARTIAL_BUGS_DIR = DATA_DIR + "partial_issues/"
PARTIAL_OPEN_ISSUES_DIR = DATA_DIR + "partial_open_issues/"
PARTIAL_OPEN_BUGS_DIR = DATA_DIR + "partial_open_bugs/"

COMMENTS_DIR = DATA_DIR + "comments/"

ISSUES_PATH = DATA_DIR + "issues.csv"
BUGS_PATH = DATA_DIR + "bugs.csv"

BUGS_WITH_FIXES_PATH = DATA_DIR + "bugs_w_fixes.csv"
BUGS_WITH_TF_IDF_PATH = DATA_DIR + "bugs_w_tf_idf.csv"
BUGS_WITH_STATS_PATH = DATA_DIR + "bugs_w_stats.csv"

ISSUE_REPR_SAMPLE_PATH = DATA_DIR + "issue_repr_sample.csv"