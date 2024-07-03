
import requests
import json
import csv
import pandas as pd
import subprocess
import time
import sys

from __global_paths import *

NUM_REPOS = 1000
ISSUES_PER_REPO = 100

if len(sys.argv) == 2:
    try:
        NUM_REPOS = int(sys.argv[1])
    except:
        raise RuntimeError(f"Usage: {sys.argv[0]} num_repos")

with open(GH_ACCESS_TOKEN + f"_0", "r") as file:
  gh_access_token = file.read().strip()

gh_query = """
    query($q: String!, $cursor: String, $issuecount: Int) {
        rateLimit {
            remaining
            cost
            used
        }
        search(query:$q, type: ISSUE, first:$issuecount, after:$cursor) {
            pageInfo {
                hasNextPage
                endCursor
            }
            nodes {
                ... on Issue {
                    id
                    title
                    body
                    url
                    comments (first:100) {
                        nodes {
                            bodyText
                        }
                    }
                }
            }
        }
    }
"""

url = "https://api.github.com/graphql"
headers = {"Authorization": f"Bearer {gh_access_token}"}

def search_issues(owner, name):
  nameWithOwner = owner + "/" + name
  count = 0
  q = f"repo:{nameWithOwner} is:issue"
  cursor = None
  remaining_issues = ISSUES_PER_REPO
  while (True):
    issuecount = remaining_issues if remaining_issues<100 else 100
    json = {"query": gh_query, "variables": {"q": q, "cursor": cursor, "issuecount": issuecount}}
    response = requests.post(url, json=json, headers=headers)

    if (response.status_code != 200):
      print(f"Key: {key}. Response code: {response.status_code}")
      time.sleep(20)
      continue

    response = response.json()

    if ("errors" in response):
      cont = False
      for error in response["errors"]:
        if "type" in error and (error["type"] == "RATE_LIMITED"):
          cont = True
      if cont:
        print("Key: {key}. Rate limited. Sleeping...")
        time.sleep(20)
        continue
      else:
        print(error)
        exit(0)

    response = response["data"]
    rateLimit = response["rateLimit"]

    hasNextPage = response["search"]["pageInfo"]["hasNextPage"]
    issues = response["search"]["nodes"]

    with open(ISSUE_REPR_SAMPLE_PATH, "a") as file:
        writer = csv.writer(file, lineterminator="\n")

        for issue in issues:
            with open(f"{COMMENTS_DIR}{issue['id']}", "w") as cfile:
                cfile.write(issue["title"] + "\n")
                cfile.write(issue["body"] + "\n")
                for c in issue["comments"]["nodes"]:
                    cfile.write(c["bodyText"] + "\n")

            row = [nameWithOwner, issue["id"], issue["title"], issue["url"]]
            writer.writerow(row)

    cursor = response["search"]["pageInfo"]["endCursor"]
    remaining_issues -= issuecount
    if (not hasNextPage) or remaining_issues<=0:
        break


def find_repr_issues():
    df = pd.read_csv(REPOS_PATH)
    subprocess.run(f"mkdir -p {COMMENTS_DIR}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print("STARTING GET DOC FREQUENCY")
    print(f"NUM_GH_KEYS: {num_gh_keys}. KEY: {key}")

    with open(ISSUE_REPR_SAMPLE_PATH, "w") as file:
        writer = csv.writer(file, lineterminator="\n")
        row = ["repoName", "id", "title", "url"]
        writer.writerow(row)

    jumpsize = df.shape[0]//NUM_REPOS
    for index, row in df[df.index % jumpsize == 0].iterrows():
        search_issues(row["owner"], row["name"])
        if (index//jumpsize)%100 == 0:
            print(f"Key: {key}. Row: {index}. ({round(100*index/df.shape[0], 2)}% Done)")

def get_keyword_counts():
    df = pd.read_csv(ISSUE_REPR_SAMPLE_PATH)
    keyword_counts = [0 for j in range(len(keywords))]
    for i, row in df.iterrows():
        index = row["id"]
        with open(f"{COMMENTS_DIR}{index}", "r") as file:
            comments = file.read()
            # print(comments)
            for j in range(len(keywords)):
                if keywords[j].lower() in comments.lower():
                    keyword_counts[j]+=1
    
    zipped = []
    for j in range(len(keywords)):
        zipped.append((keyword_counts[j], keywords[j]))
    zipped.sort()
    for z in zipped:
       print(z[1].ljust(20), z[0])


if __name__ == "__main__":
    find_repr_issues()
    get_keyword_counts()
