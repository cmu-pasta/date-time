import requests
import json
import csv
import pandas as pd
import subprocess

from __global_paths import *

with open(GH_ACCESS_TOKEN, "r") as file:
  gh_access_token = file.read().strip()

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

with open(OPEN_ISSUES_PATH, "w") as file:
  writer = csv.writer(file, lineterminator="\n")
  
  row = ["repoName", "title", "bodyHtml", "url", "lockReason", "labels"]
  writer.writerow(row)

import time

url = "https://api.github.com/graphql"
headers = {"Authorization": f"Bearer {gh_access_token}"}

def search_issues(nameWithOwner):
  count = 0
  q = f"repo:{nameWithOwner} is:issue is:open in:title \"datetime\" OR \"DST\" OR \"daylight saving\" OR \"utc\" OR \"time zone\""
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

    with open(OPEN_ISSUES_PATH, "a") as file:
      writer = csv.writer(file, lineterminator="\n")

      for issue in issues:
        labels = []
        for l in issue["labels"]["nodes"]:
          labels.append(l["name"])

        row = [nameWithOwner, issue["title"], "<html redacted>", issue["url"], # issue["bodyHTML"]
               issue["activeLockReason"], labels
        ]
        writer.writerow(row)
        count += 1

    cursor = response["search"]["pageInfo"]["endCursor"]
    if (not hasNextPage):
      break
  print(f"{nameWithOwner} Completed. Count: {count}")


print("STARTING GET_ISSUES")


df = pd.read_csv(SEPARATED_FILTERED_REPOS_PATH)

for index, row in df.iterrows():
  nameWithOwner = row["owner"] + "/" + row["name"]
  search_issues(nameWithOwner)

subprocess.run(f"head -n 1 {OPEN_ISSUES_PATH} > {OPEN_BUGS_PATH}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
subprocess.run(f"grep -E '(bug|fix|wrong)' {OPEN_ISSUES_PATH} >> {OPEN_BUGS_PATH}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
