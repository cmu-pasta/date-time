DATA_DIR = "/data/sjoukov/date-time/data/"

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
KEYWORDS = []
for start in range(0, len(KEYWORDS_RAW), 6):
    KEYWORDS.append(KEYWORDS_RAW[start:start+6])

KEYWORDS_LIST_LEN = 7

NUM_GH_ACCESS_TOKENS = 7

GH_ACCESS_TOKEN = "access_tokens/gh_access_token"
SG_ACCESS_TOKEN = "access_tokens/sg_access_token"

LOG_DIR = DATA_DIR + "logs/"
CLONE_REPOS_DIR = DATA_DIR + "cloned_repos/"

REPOS_PATH = DATA_DIR + "repos.csv"
SEPARATED_FILTERED_REPOS_PATH = DATA_DIR + "repos_with_separated_grep.csv"

ISSUES_PATH = DATA_DIR + "issues.csv"
BUGS_PATH = DATA_DIR + "bugs.csv"
OPEN_ISSUES_PATH = DATA_DIR + "open_issues.csv"
OPEN_BUGS_PATH = DATA_DIR + "open_bugs.csv"
COMMENTS_DIR = DATA_DIR + "comments/"

CONCAT_ISSUES_PATH = DATA_DIR + "concat_issues.csv"
CONCAT_BUGS_PATH = DATA_DIR + "concat_bugs.csv"

FILTERED_BUGS_PATH = DATA_DIR + "filtered_bugs.csv"

TF_IDF_BUGS_PATH = DATA_DIR + "tf_idf_bugs.csv"
