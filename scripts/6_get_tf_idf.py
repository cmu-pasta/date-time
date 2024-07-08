from __global_paths import *
import pandas as pd
import numpy as np
import math
import sys
import re
from nltk.tokenize import word_tokenize

IDF_SOURCE = "repr"
if len(sys.argv) == 2:
    if sys.argv[1] not in ["repr", "filtered"]:
        raise RuntimeError(f"Usage: {sys.argv[0]} [repr/filtered]")
    IDF_SOURCE = sys.argv[1]

# By default, nltk doesn't come with all the data it needs to run, so we need to run this download command
# to grab the rest of the data
try:
    word_tokenize("test")
except:
    import nltk
    nltk.download('punkt')

def tokenize(text):
    tokens = word_tokenize(text)
    # only include tokens that contain a letter
    # this will also include things like the "'s" in it's -> ["it", "'s"]
    tokens = [t for t in tokens if re.search("[a-zA-Z]", t) is not None]
    return tokens

# a word matches if it contains the keyword as a prefix. 
# Since this will catch plurals, we only use singular keywords
def count_matches(tokens):
    ans = np.zeros(len(KEYWORDS_SINGULAR))
    for i,keyword in enumerate(KEYWORDS_SINGULAR):
        for word in tokens:
            if word.lower().startswith(keyword.lower()):
                ans[i] += 1
    return ans

def compute_tf(comments):
    words = tokenize(comments)
    word_count = len(words)
    if word_count == 0:
        return np.zeros(len(KEYWORDS_SINGULAR))
    return count_matches(words) / word_count

repr_df = pd.read_csv(ISSUE_REPR_SAMPLE_PATH)
bugs_df = pd.read_csv(BUGS_WITH_FIXES_PATH)

# calculate IDF
idf_df = repr_df if IDF_SOURCE == "repr" else bugs_df
keyword_counts = np.ones(len(KEYWORDS_SINGULAR))
issuecount = 0
for i, row in idf_df.iterrows():
    index = row["id"]
    with open(f"{COMMENTS_DIR}{index}", "r") as file:
        comments = file.read()
        words = tokenize(comments)
        appearances = count_matches(words)
        for j in range(len(KEYWORDS_SINGULAR)):
            if appearances[j] != 0:
                keyword_counts[j]+=1
    
print("Finished calculating TF-IDF")

idf = np.log(repr_df.shape[0] / keyword_counts)
pd.DataFrame(idf, columns=["idf"]).to_csv(IDFS_PATH, index=False)

# calculate tf-idf
for i, row in bugs_df.iterrows():
    index = row["id"]
    with open(f"{COMMENTS_DIR}{index}", "r") as file:
        comments = file.read()
        tf = compute_tf(comments)
        indivivdual_tf_idf = tf * idf
        for j, word in enumerate(KEYWORDS_SINGULAR):
            bugs_df.at[i, "td_idf_"+word] = indivivdual_tf_idf[j]
        tf_idf = tf.dot(idf)
        bugs_df.at[i, "tf_idf"] = tf_idf
bugs_df.to_csv(BUGS_WITH_TF_IDF_PATH, index=False)
