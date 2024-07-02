import requests
import json
import csv

from __global_paths import *

with open(GH_ACCESS_TOKEN, "r") as file:
    gh_access_token = file.read().strip()

query = """
query($q: String!, $cursor: String) {
  rateLimit {
    remaining
    cost
    used
  }
  search(query:$q, type: REPOSITORY, first: 100, after:$cursor) {
		pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        nameWithOwner
        owner {
          login
        }
        name
        url
        description
        stargazerCount
        primaryLanguage {
          name
        }
        updatedAt
        createdAt
        issues {
          totalCount
        }
        forkCount
        watchers {
          totalCount
        }
        discussions {
          totalCount
        }
      }
    }
  }
}
"""

with open(REPOS_PATH, "w") as file:
  writer = csv.writer(file, lineterminator="\n")
  
  row = ["nameWithOwner", "owner", "name", "url", "description",
         "stars", "primaryLanguage", "updatedAt",
         "createdAt", "issuesCount", "forkCount",
         "watchersCount", "discussionsCount"
  ]
  writer.writerow(row)

url = "https://api.github.com/graphql"
headers = {"Authorization": f"Bearer {gh_access_token}"}

def get_repos_between_dates(min_date_str=None, max_date_str=None):
  count = 0
  
  cursor = None

  if (min_date_str == None):
    min_date_str = "2014-06-01"
  if (max_date_str == None):
    max_date_str = "2024-06-01"

  q = f"created:{min_date_str}..{max_date_str} stars:>100 language:Python"

  while (True):
    
    count += 1
    
    json = {"query": query, "variables": {"q": q, "cursor": cursor}}
    
    response = requests.post(url, json=json, headers=headers).json()
    if (not "data" in response.keys()):
      print(f"{q}: bad response!!!\n RESPONSE: {response}")
      return False
    response = response["data"]

    rateLimit = response["rateLimit"]
    hasNextPage = response["search"]["pageInfo"]["hasNextPage"]
    cursor = response["search"]["pageInfo"]["endCursor"]

    repos = response["search"]["nodes"]

    with open(REPOS_PATH, "a") as file:
      writer = csv.writer(file, lineterminator="\n")

      for repo in repos:
        row = [repo["nameWithOwner"], repo["owner"]["login"], repo["name"], 
               repo["url"], repo["description"],
               repo["stargazerCount"], repo["primaryLanguage"]["name"], repo["updatedAt"],
               repo["createdAt"], repo["issues"]["totalCount"], repo["forkCount"],
               repo["watchers"]["totalCount"], repo["discussions"]["totalCount"]
        ]
        writer.writerow(row)

    if (not hasNextPage):
      print(f"{min_date_str}..{max_date_str}, Requests: {count}, Remaining: {rateLimit['remaining']}")
      break
  return True

date_ranges = []

for i in range(126):
  min_date_year = 2014 + i // 12
  min_date_month = 1 + i % 12
  
  max_date_year = 2014 + (i+1) // 12
  max_date_month = 1 + (i+1) % 12
  
  date_ranges.append((f"{min_date_year}-{min_date_month:02}-02", f"{max_date_year}-{max_date_month:02}-01"))

for date_range in date_ranges:
  if (not get_repos_between_dates(min_date_str=date_range[0], max_date_str=date_range[1])):
    break
