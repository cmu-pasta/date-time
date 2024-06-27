import requests
import json
import csv
import pandas as pd
import subprocess
import time
import sys
import re

from __global_paths import *

keywords = [
  "datetime OR timestamp OR date OR time OR tzinfo OR calendar",
  "pytz OR dateutil OR arrow OR whenever OR pendulum OR heliclockter",
  "leap OR DST OR daylight OR year OR localtime OR epoch",
  "strptime OR strftime OR utcnow OR fromtimestamp OR GMT OR UTC",
  "interval OR duration OR elapsed OR timedelta OR fold",
  "microsecond OR nanosecond OR millisecond OR second"
]

open_or_closed = "closed"
key = 0

if len(sys.argv) >= 2:
    open_or_closed = sys.argv[1]
if len(sys.argv) >= 3:
    try:
        key = int(sys.argv[2])
    except:
        raise RuntimeError(f"Usage: {sys.argv[0]} [open/closed] [0-5]")
if key < 0 or key > 5 or (open_or_closed != "open" and open_or_closed != "closed"):
   raise RuntimeError(f"Usage: {sys.argv[0]} [open/closed] [0-5]")

WRITE_ISSUES_PATH = ISSUES_PATH if open_or_closed == "closed" else OPEN_ISSUES_PATH
WRITE_BUGS_PATH   = BUGS_PATH   if open_or_closed == "closed" else OPEN_BUGS_PATH

WRITE_ISSUES_PATH += f"_{key}"
WRITE_BUGS_PATH += f"_{key}"

with open(GH_ACCESS_TOKEN + f"_{key%4}", "r") as file:
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
                    title
                    bodyHTML
                    url
                    activeLockReason
                    comments (first:100) {
                        totalCount
                        nodes {
                            bodyText
                        }
                    }
                    labels (first:100) {
                    nodes {
                        name
                    }
                }
            }
        }
    }
}
"""
 
url = "https://api.github.com/graphql"
headers = {"Authorization": f"Bearer {gh_access_token}"}
pattern = r'https?://[^\\"]*pull[^\\"]*'

def search_issues(nameWithOwner):
  count = 0
  q = f"repo:{nameWithOwner} is:issue is:{open_or_closed} in:title {keywords[key]}"
  cursor = None
  while (True):
    json = {"query": gh_query, "variables": {"q": q, "cursor": cursor}}
    response = requests.post(url, json=json, headers=headers)

    if (response.status_code != 200):
      print(f"Response code: {response.status_code}")
      time.sleep(20)
      continue

    response = response.json()

    if ("errors" in response):
      cont = False
      for error in response["errors"]:
        if (error["type"] == "RATE_LIMITED"):
          cont = True
      if cont:
        print("Rate limited. Sleeping...")
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
        fixURL = ""
        for l in issue["labels"]["nodes"]:
          labels.append(l["name"])
        for comment in issue["comments"]["nodes"]:
          html = comment["bodyText"]
          fixURL += html
          if "/pull/" in html:
              fixURL += "FOUND!"
          matches = re.findall(pattern, html)
         # if matches:
         #   fixURL = matches[0]
         #   break

        row = ["", "", "", "", "", "", fixURL]
        #row = [nameWithOwner, issue["title"], issue["url"], issue["activeLockReason"], issue["comments"]["totalCount"], labels, fixURL]
        writer.writerow(row)

    cursor = response["search"]["pageInfo"]["endCursor"]
    if (not hasNextPage):
      break


def main():

  print("STARTING GET_ISSUES")
  print(f"KEY: {key}. KEYWORDS: {keywords[key]}")

  with open(WRITE_ISSUES_PATH, "w") as file:
    writer = csv.writer(file, lineterminator="\n")
    row = ["repoName", "title", "url", "lockReason", "commentsCount", "labels", "fixURL"]
    writer.writerow(row)

  for index, row in df.iterrows():
    nameWithOwner = row["owner"] + "/" + row["name"]
    search_issues(nameWithOwner)
    if (index % 100 == 0):
      print(f"Finished row {index} ({round(100*index/df.shape[0], 2)}% Done)")
      # print(f"{nameWithOwner} completed")

  subprocess.run(f"head -n 1 {WRITE_ISSUES_PATH} > {WRITE_BUGS_PATH}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  subprocess.run(f"grep -E '(bug|fix|wrong)' {WRITE_ISSUES_PATH} >> {WRITE_BUGS_PATH}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


if __name__ == "__main__":
  main()
