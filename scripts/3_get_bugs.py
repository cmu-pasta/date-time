import requests
import json
import csv
import pandas as pd
import subprocess
import time
import sys
import re

from __global_paths import *

KEYWORDS_WITH_OR = [" OR ".join(KEYWORDS[i]) for i in range(len(KEYWORDS))]
print(KEYWORDS_WITH_OR)

open_or_closed = "closed"
key = 0

if len(sys.argv) == 3:
    try:
        key = int(sys.argv[2])
    except:
        raise RuntimeError(f"Usage: {sys.argv[0]} [open/closed] key")
    if key < 0 or key >= len(KEYWORDS_WITH_OR):
        raise RuntimeError(f"key must be between 0 and {len(KEYWORDS_WITH_OR)}")
    if (open_or_closed != "open" and open_or_closed != "closed"):
        raise RuntimeError(f"Usage: {sys.argv[0]} [open/closed] key")


WRITE_ISSUES_PATH = ISSUES_PATH if open_or_closed == "closed" else OPEN_ISSUES_PATH
WRITE_BUGS_PATH   = BUGS_PATH   if open_or_closed == "closed" else OPEN_BUGS_PATH

WRITE_ISSUES_PATH += f"_{key}"
WRITE_BUGS_PATH += f"_{key}"

with open(GH_ACCESS_TOKEN + f"_{key%NUM_GH_ACCESS_TOKENS}", "r") as file:
  gh_access_token = file.read().strip()

df = pd.read_csv(SEPARATED_FILTERED_REPOS_PATH[:-4] + "_filtered.csv")

gh_query = """
    query($q: String!, $cursor: String) {
        rateLimit {
            remaining
            cost
            used
        }
        search(query:$q, type: ISSUE, first: 100, after:$cursor) {
            pageInfo {
                hasNextPage
                endCursor
            }
            nodes {
                ... on Issue {
                    id
                    title
                    bodyHTML
                    url
                    activeLockReason
                    labels (first:100) {
                        nodes {
                            name
                        }
                    }
                    comments (first:100) {
                        nodes {
                            bodyText
                        }
                    }
                    timelineItems(first:100){
                        totalCount
                        nodes {
                            ... on CrossReferencedEvent {
                                source{
                                    ... on PullRequest{
                                        permalink
                                    }
                                }
                            }
                            ... on ReferencedEvent {
                                commit{
                                    commitUrl
                                }
                            }
                            ... on ClosedEvent {
                                closer{
                                    ... on Commit {
                                        commitUrl
                                    }
                                    ... on PullRequest {
                                        permalink
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
"""

timeline_checks = [
  ["source", "permalink"],
  ["commit", "commitUrl"],
  ["closer", "commitUrl"],
  ["closer", "permalink"],
]

url = "https://api.github.com/graphql"
headers = {"Authorization": f"Bearer {gh_access_token}"}
pattern = r'\\"https?:\/\/[^\\]*pull[^\\]*\\"'

def search_issues(owner, name):
  nameWithOwner = owner + "/" + name
  count = 0
  q = f"repo:{nameWithOwner} is:issue is:{open_or_closed} in:title {KEYWORDS_WITH_OR[key]}"
  cursor = None
  while (True):
    json = {"query": gh_query, "variables": {"q": q, "cursor": cursor}}
    response = requests.post(url, json=json, headers=headers)

    if (response.status_code != 200):
      print(f"Key: {key}. Response code: {response.status_code}")
      time.sleep(20)
      continue

    response = response.json()

    if ("errors" in response):
      cont = False
      for error in response["errors"]:
        if (error["type"] == "RATE_LIMITED"):
          cont = True
      if cont:
        print("Key: {key}. Rate limited. Sleeping...")
        time.sleep(20)
        continue
      else:
        exit(0)

    response = response["data"]
    rateLimit = response["rateLimit"]

    hasNextPage = response["search"]["pageInfo"]["hasNextPage"]
    issues = response["search"]["nodes"]

    with open(WRITE_ISSUES_PATH, "a") as file:
        writer = csv.writer(file, lineterminator="\n")

        for issue in issues:
            labels = []
            comments = []
            fixURL = ""
            fixURLcount = 0
            for l in issue["labels"]["nodes"]:
                labels.append(l["name"])
            with open(f"{COMMENTS_DIR}{issue['id']}", "w") as cfile:
                for c in issue["comments"]["nodes"]:
                    cfile.write(c["bodyText"] + "\n")
            for tl_item in issue["timelineItems"]["nodes"]:
                if tl_item is None: continue
                # walk down the paths
                for tl_path in timeline_checks:
                    tl_curr = tl_item
                    good = True
                    for obj_name in tl_path:
                        if obj_name in tl_curr:
                            tl_curr = tl_curr[obj_name]
                            if tl_curr is None:
                                good = False
                                break
                        else:
                            good = False
                            break
                    if good:
                        if fixURL == "":
                            fixURL = tl_curr
                        fixURLcount += 1

            # row = ["", "", "", "", "", "", fixURL, fixURLcount]
            row = [nameWithOwner, issue["id"], issue["title"], issue["url"], issue["activeLockReason"], issue["timelineItems"]["totalCount"], labels, fixURL, fixURLcount]
            writer.writerow(row)

    cursor = response["search"]["pageInfo"]["endCursor"]
    if (not hasNextPage):
        break


def main():
  subprocess.run(f"mkdir -p {COMMENTS_DIR}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

  print("STARTING GET_ISSUES")
  print(f"NUM_GH_ACCESS_TOKENS: {NUM_GH_ACCESS_TOKENS}. KEY: {key}. KEYWORDS: {KEYWORDS_WITH_OR[key]}")

  with open(WRITE_ISSUES_PATH, "w") as file:
    writer = csv.writer(file, lineterminator="\n")
    row = ["repoName", "id", "title", "url", "lockReason", "timelineCount", "labels", "fixUrl", "fixUrlCount"]
    writer.writerow(row)

  for index, row in df.iterrows():
    search_issues(row["owner"], row["name"])
    if (index % 100 == 0):
        print(f"Key: {key}. Row: {index}. ({round(100*index/df.shape[0], 2)}% Done)")
      # print(f"{nameWithOwner} completed")

  # No longer needed as "fix" now appears in the header
  # subprocess.run(f"head -n 1 {WRITE_ISSUES_PATH} > {WRITE_BUGS_PATH}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  subprocess.run(f"grep -iE '(bug|fix|wrong)' {WRITE_ISSUES_PATH} >> {WRITE_BUGS_PATH}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


if __name__ == "__main__":
  main()
