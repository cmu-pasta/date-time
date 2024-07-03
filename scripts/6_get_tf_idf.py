from __global_paths import *
import pandas as pd
import numpy as np
import math

keywords = """
datetime        pytz    leap    strptime        microsecond
timestamp       dateutil        DST     strftime        nanosecond
tzinfo  arrow   daylight        utcnow  millisecond
epoch   pendulum        year    fromtimestamp   timezone
timedelta       UTC     localtime       GMT     interval
fold    elapsed duration        month
""".split()

def compute_idf(comments):
    num_documents = len(comments)
    idf = []
    for keyword in keywords:
        containing_docs = sum(1 for comment in comments if keyword in comment.split())
        idf_score = math.log(num_documents / (1 + containing_docs))
        idf.append(idf_score)
    return idf

def compute_tf(comment):
    words = comment.split()
    word_count = len(words)
    if word_count == 0:
        return np.zeros(len(keywords))
    tf = np.array([words.count(keyword) / word_count for keyword in keywords])
    return tf

# calculate IDF
repr_df = pd.read_csv(ISSUE_REPR_SAMPLE_PATH)
keyword_counts = np.zeros(len(keywords))
issuecount = 0
for i, row in repr_df.iterrows():
    index = row["id"]
    with open(f"{COMMENTS_DIR}{index}", "r") as file:
        comments = file.read()
        for j in range(len(keywords)):
            if keywords[j].lower() in comments.lower():
                keyword_counts[j]+=1

idf = np.log(keyword_counts / repr_df.shape[0])

# calculate tf-idf
bugs_df = pd.read_csv(FILTERED_BUGS_PATH)
for i, row in bugs_df.iterrows():
    index = row["id"]
    with open(f"{COMMENTS_DIR}{index}", "r") as file:
        comments = file.read()
        tf = compute_tf(comments)
        tf_idf = tf.dot(idf)
        bugs_df.at[i, "tf_idf"] = tf_idf

bugs_df.to_csv(TF_IDF_BUGS_PATH, index=False)
