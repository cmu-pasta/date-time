from __global_paths import *
import pandas as pd
import numpy as np
import math
import re
from nltk.tokenize import word_tokenize

try:
    word_tokenize("test")
except:
    import nltk
    nltk.download('punkt')

def tokenize(comment):
    tokens = word_tokenize(comment)
    tokens = [t for t in tokens if re.search("[a-zA-Z]", t) is not None]
    return tokens

def count_matches(tokens):
    ans = np.zeros(len(KEYWORDS_SINGULAR))
    for i,keyword in enumerate(KEYWORDS_SINGULAR):
        for word in tokens:
            if word.lower().startswith(keyword.lower()):
                ans[i] += 1
    return ans

def compute_tf(comment):
    words = tokenize(comment)
    # words = comment.split()
    word_count = len(words)
    if word_count == 0:
        return np.zeros(len(KEYWORDS_SINGULAR))
    return count_matches(words) / word_count

# calculate IDF
repr_df = pd.read_csv(ISSUE_REPR_SAMPLE_PATH)
keyword_counts = np.ones(len(KEYWORDS_SINGULAR))
issuecount = 0
for i, row in repr_df.iterrows():
    index = row["id"]
    with open(f"{COMMENTS_DIR}{index}", "r") as file:
        comment = file.read()
        words = tokenize(comment)
        appearances = count_matches(words)
        for j in range(len(KEYWORDS_SINGULAR)):
            if appearances[j] != 0:
                keyword_counts[j]+=1
    

idf = np.log(repr_df.shape[0] / keyword_counts)
pd.DataFrame(idf, columns=["idf"]).to_csv(IDFS_PATH, index=False)

# calculate tf-idf
bugs_df = pd.read_csv(BUGS_WITH_FIXES_PATH)
for i, row in bugs_df.iterrows():
    index = row["id"]
    with open(f"{COMMENTS_DIR}{index}", "r") as file:
        comments = file.read()
        # bugs_df.at[i, "comments"] = comments
        tf = compute_tf(comments)
        tf_idf = tf.dot(idf)
        bugs_df.at[i, "tf_idf"] = tf_idf
        bugs_df.at[i, "size"] = len(comments)

bugs_df.to_csv(BUGS_WITH_TF_IDF_PATH, index=False)
