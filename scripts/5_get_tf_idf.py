from __global_paths import *
import pandas as pd
import math

bugs_df = pd.read_csv(CONCAT_BUGS_PATH)
# comments = {}

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
        return [0] * len(keywords)
    tf = [words.count(keyword) / word_count for keyword in keywords]
    return tf

# indices = [row["id"] for _, row in bugs.iterrows()]
for i, row in bugs_df.iterrows():
# for index in indices:
    index = row["id"]
    with open(f"{COMMENTS_DIR}{index}", "r") as file:
        comments = file.read()
        bugs_df.at[i, "comments"] = comments
        tf = compute_tf(comments)
        for j, keyword in enumerate(keywords):
            bugs_df.at[i, keyword] = tf[j]
        # bugs_df.at[i, keywords] = 

idf_scores = compute_idf(bugs_df["comments"])
idf_series = pd.Series(idf_scores, index=keywords)

print(len(bugs_df[keywords]))
print(len(idf_scores))

bugs_df["tf_idf"] = bugs_df[keywords].dot(idf_series)

bugs_df.drop(columns=keywords, axis=1, inplace=True)

# print(bugs_df)

bugs_df.to_csv(CONCAT_TF_IDF_BUGS_PATH, index=False)

# tf_scores = []

# for index in indices:
    # tf_scores[index] = compute_tf()

# tf_scores = {compute_tf(index, keywords) for index in comments.keys()}

# print(len(tf_scores))
