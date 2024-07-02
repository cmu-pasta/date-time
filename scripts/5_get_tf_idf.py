from __global_paths import *
import pandas as pd
import math
import re

bugs_df = pd.read_csv(FILTERED_BUGS_PATH)

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
    words = re.split(r'[^a-zA-Z]+', comment)
    # words = comment.split()
    word_count = len(words)
    if word_count == 0:
        print("word count is zero!!!")
        return [0] * len(keywords)
    tf = [(len([word for word in words if word.startswith(keyword)])) / word_count for keyword in keywords]
    return tf

for i, row in bugs_df.iterrows():
    index = row["id"]
    with open(f"{COMMENTS_DIR}{index}", "r") as file:
        comments = file.read() + " " + row["title"]
        bugs_df.at[i, "comments"] = comments
        tf = compute_tf(comments)
        for j, keyword in enumerate(keywords):
            bugs_df.at[i, keyword] = tf[j]

idf_scores = compute_idf(bugs_df["comments"])
idf_series = pd.Series(idf_scores, index=keywords)

bugs_df["tf_idf"] = bugs_df[keywords].dot(idf_series)

bugs_df.drop(columns=keywords + ["comments"], axis=1, inplace=True)

bugs_df.to_csv(TF_IDF_BUGS_PATH, index=False)
