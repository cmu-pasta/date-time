import requests
from __global_paths import *

key = 1
with open(GH_ACCESS_TOKEN + f"_{key%4}", "r") as file:
  gh_access_token = file.read().strip()

gh_query = """
    query($q: String!, $cursor: String) {
        rateLimit {
            remaining
            cost
            used
        }
        search(query:$q, type: ISSUE, first: 1, after:$cursor) {
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
                        }
                    }
                }
            }
        }
    }
"""


url = "https://api.github.com/graphql"
headers = {"Authorization": f"Bearer {gh_access_token}"}
pattern = r'\\"https?:\/\/[^\\]*pull[^\\]*\\"'

query_words = "SERVER_TIMESTAMP"
q = f"repo:googleapis/google-cloud-python is:issue is:closed in:title {query_words}"
json = {"query": gh_query, "variables": {"q": q, "cursor": None}}
response = requests.post(url, json=json, headers=headers)
if (response.status_code != 200):
    print(f"Response code: {response.status_code}")
elif ("errors" in response.json()):
    print(response.json())
else:
    print(response.json()["data"])