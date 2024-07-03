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
                    body
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
                            __typename
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
                                    __typename
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
# q = f"repo:googleapis/google-cloud-python is:issue is:closed in:title {query_words}"
q = "repo:sdispater/pendulum type:issue \"difference in days is incorrect across daylight savings\""
# q = "repo:sdispater/pendulum type:issue \"provide wheel for python3.11-windows\""
# q = "repo:googleapis/google-cloud-python datetime OR timestamp OR tzinfo OR epoch OR timedelta OR fold OR year OR month"

json = {"query": gh_query, "variables": {"q": q, "cursor": None}}
response = requests.post(url, json=json, headers=headers)
if (response.status_code != 200):
    print(f"Response code: {response.status_code}")
elif ("errors" in response.json()):
    print(response.json())
else:
    print(response.json()["data"])