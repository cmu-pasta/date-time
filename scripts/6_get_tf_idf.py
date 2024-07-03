from __global_paths import *
import pandas as pd
import numpy as np
import math
import re

def compute_tf(comment):
    words = re.split(r'[^a-zA-Z]+', comment)
    # words = comment.split()
    word_count = len(words)
    if word_count == 0:
        return np.zeros(len(KEYWORDS_RAW))
    tf = np.array([(len([word for word in words if word.lower().startswith(keyword.lower())])) / word_count for keyword in KEYWORDS_RAW])
    return tf

# calculate IDF
repr_df = pd.read_csv(ISSUE_REPR_SAMPLE_PATH)
keyword_counts = np.zeros(len(KEYWORDS_RAW))
issuecount = 0
for i, row in repr_df.iterrows():
    index = row["id"]
    with open(f"{COMMENTS_DIR}{index}", "r") as file:
        comment = file.read()
        words = re.split(r'[^a-zA-Z]+', comment)
        appearances = [(len([word for word in words if word.lower().startswith(keyword.lower())])) for keyword in KEYWORDS_RAW]
        for j in range(len(KEYWORDS_RAW)):
            if appearances[j] != 0:
                keyword_counts[j]+=1
    

idf = np.log(repr_df.shape[0] / keyword_counts)
pd.DataFrame(idf, columns=["idf"]).to_csv(IDFS_PATH, index=False)
exit(0)

# calculate tf-idf
bugs_df = pd.read_csv(BUGS_WITH_FIXES_PATH)
for i, row in bugs_df.iterrows():
    index = row["id"]
    with open(f"{COMMENTS_DIR}{index}", "r") as file:
        comments = file.read()
        bugs_df.at[i, "comments"] = comments
        tf = compute_tf(comments)
        tf_idf = tf.dot(idf)
        bugs_df.at[i, "tf_idf"] = tf_idf

bugs_df.to_csv(BUGS_WITH_TF_IDF_PATH, index=False)
